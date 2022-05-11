

NumberOFAtrributes = 0

import math
import multiprocessing
import os

import pandas as pd
import numpy as np

from gensim.models import Word2Vec


class WordEmbedding:
    def __init__(self):
        #print(">>> ml > embedding.py > WordEmbedding : __init__()")

        self.embedding = None
        self.dim = None
        print("start training embedding")

    # def describing(self, Indata):
    # describe = {}
    # for j in range(0, len(Indata.columns.values)):
    #     valueList = []
    #     valueList.append(len(Indata.iloc[:, j].unique()))
    #     valueList.append(
    #         round(len(Indata.iloc[:, j].unique())/Indata.shape[0], 3))
    #     describe[Indata.columns.values[j]] = valueList
    # # print(describe)
    # return describe

    def fit(
        self,
        sentences,
        gbs,
        dim=20,
        window=1,
        min_count=1,
        negative=20,
        iter=30,
        workers=30,
        NG=1,
    ):
        #print(">>> ml > embedding.py > WordEmbedding : fit()")

        # print(NG)# number of group by attributes
        w2v = Word2Vec(
            sentences,
            size=int(dim / NG),
            window=1,
            min_count=1,
            negative=30,
            iter=iter,
            workers=multiprocessing.cpu_count(),
        )  # ,ns_exponent=0.0
        word_vectors = w2v.wv  # Matix of model
        vocab = w2v.wv.vocab  # Vocabulary
        self.dim = dim

        count = 0
        Group = {}

        count = 0
        for each in vocab:
            if "gb" in each:
                Group[each.split(",@,")[1]] = word_vectors.vectors[count]
            count = count + 1

        del word_vectors  ############################
        del vocab  ############################
        self.embedding = Group

        print("finish training embedding")
        return Group

    def predict(self, key):
        #print(">>> ml > embedding.py > WordEmbedding : predict()")

        return self.embedding[key]

    def predicts_low_efficient(self, keys):
        #print(">>> ml > embedding.py > WordEmbedding : predicts_low_efficient()")

        results = np.array(self.embedding[keys[0]])

        for key in keys[1:]:

            results = np.vstack((results, self.embedding[key]))

        return results

    def predicts(self, keys):
        #print(">>> ml > embedding.py > WordEmbedding : predicts()")

        print("start embedding inference")

        results = []

        # print("keys are ")
        # print(self.embedding.keys())
        # print("size is ", len(self.embedding))
        # exit()

        for key in keys:
            # print("predict key")
            # print(key)
            # print(type(key))
            # print(len(key))
            if len(key) >= 2:
                ttt = list(self.embedding[key[0] + "_" + str(0)])

                for i in range(1, len(key)):
                    ttt1 = list(self.embedding[key[i] + "_" + str(i)])

                    ttt = ttt + ttt1

                results.append(ttt)
                # print(len(ttt))
            else:

                ttt = list(self.embedding[key[0] + "_" + str(0)])

                # for i in range(1,len(key)):
                #    ttt1=list(self.embedding[key[i]])
                #    ttt=ttt+ttt1

                results.append(ttt)

        results = np.reshape(results, (-1, self.dim))

        print("end embedding inference")

        return results


def dataframe2sentences(df: pd.DataFrame, gbs: list):
    #print(">>> ml > embedding.py > None : dataframe2sentences()")

    headers = df.columns  # .to_list()
    sentences = []
    no_gbs = list(set(headers) - set(gbs))
    # print(gbs)
    for row in df.itertuples():

        CCC = 0
        for gb in gbs:
            while CCC < len(str(getattr(row, gb)).split(",")):
                front_words = []

                front_words.append(
                    gb + ",@," + str(getattr(row, gb)).split(",")[CCC] + "_" + str(CCC)
                )
                CCC = CCC + 1

                for no_gb in no_gbs:
                    each_sentence = list(front_words)
                    each_sentence.append(no_gb + ",@," + str(getattr(row, no_gb)))
                    sentences.append(each_sentence)

    return sentences


def columns2sentences(gbs_data, xs_data, ys_data=None):
    #print(">>> ml > embedding.py > None : columns2sentences()")

    NumberOFAtrributes = len(gbs_data[0])

    new_gbs_data = []
    # print((gbs_data))
    for k in range(0, len(gbs_data)):
        temp = ""
        for i in range(0, NumberOFAtrributes):
            temp = temp + gbs_data[k][i] + ","

        new_gbs_data.append(temp[:-1])

    gbs_data = new_gbs_data
    # print((gbs_data))
    if ys_data is None:
        df = pd.DataFrame({"gb": gbs_data, "x": xs_data})
    else:

        df = pd.DataFrame({"gb": gbs_data, "x": xs_data, "y": ys_data})

    # print(df.gb)

    return dataframe2sentences(df, ["gb"])


if __name__ == "__main__":
    #print(">>> ml > embedding.py > None : __main__()")

    from datetime import datetime

    header = [
        "ss_sold_date_sk",
        "ss_sold_time_sk",
        "ss_item_sk",
        "ss_customer_sk",
        "ss_cdemo_sk",
        "ss_hdemo_sk",
        "ss_addr_sk",
        "ss_store_sk",
        "ss_promo_sk",
        "ss_ticket_number",
        "ss_quantity",
        "ss_wholesale_cost",
        "ss_list_price",
        "ss_sales_price",
        "ss_ext_discount_amt",
        "ss_ext_sales_price",
        "ss_ext_wholesale_cost",
        "ss_ext_list_price",
        "ss_ext_tax",
        "ss_coupon_amt",
        "ss_net_paid",
        "ss_net_paid_inc_tax",
        "ss_net_profit",
        "none",
    ]
    file = "/Users/scott/Documents/workspace/data/tpcds/10g/ss_10g_20.csv"
    df = pd.read_csv(
        file,
        sep="|",
        names=header,
        usecols=["ss_sales_price", "ss_sold_date_sk", "ss_store_sk"],
    )
    # print(df)
    sentenses = dataframe2sentences(df, gbs=["ss_store_sk"])
    word_embedding = WordEmbedding()
    word_embedding.fit(sentenses, gbs=["ss_store_sk"])
    # print(word_embedding.predict('92'))
    # print("*"*20)
    t1 = datetime.now()
    # print(word_embedding.predicts(['92','70','4']))
    t2 = datetime.now()
    print("time cost is ", (t2 - t1).total_seconds())

    t1 = datetime.now()
    print(word_embedding.predicts_low_efficient(["92", "70", "4"]))
    t2 = datetime.now()
    print("time cost is ", (t2 - t1).total_seconds())
    # # file_name, Max_rate,groupby_column,Embedding_dimension_size,number_of_iteration
    # word_embedding.fit("/data/tpcds/40G/ss_600k_headers.csv",
    #                    0.2, "ss_store_sk", 20, 1)
