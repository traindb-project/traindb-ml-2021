
import re
from itertools import chain

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from matplotlib.pyplot import axis, legend


def read_results(file, b_remove_null=True, split_char="\s"):
    """read the group by value and the corresponding aggregate within
    a given range, used to compare the accuracy.the

    Output: a dict contating the

    Args:
        file (file): path to the file
    """

    key_values = {}
    with open(file) as f:
        # print("Start reading file " + file)
        index = 1
        for line in f:
            # ignore empty lines

            if line != "":
                if line.strip():
                    # print(line)
                    key_value = line.replace(
                        "(", " ").replace(")", " ").replace(";", "").replace("\n", "").replace(" ","")  # .replace(",", "")
                    # print(key_value)
                    # self.logger.logger.info(key_value)
                    key_value = re.split(split_char, key_value)
                    # print("key_value", key_value)
                    # print(','.join(key_value[:-1]))

                    for i in range(2):
                        if key_value[i] == 'NULL':
                            key_value[i] = ""
                    # print(line)
                    # print(key_value)
                    if key_value[-1]=="":
                        key_value[-1]="0.0"
                    key_values[','.join(key_value[:-1])] = float(key_value[-1])

    # if ('NULL' in key_values) and b_remove_null:
    #     key_values.pop('NULL', None)
    # if ('0' in key_values) and b_remove_null:
    #     key_values.pop('0', None)


    # cnt=0
    # for key in key_values:
    #     cnt+=1
    #     print(key, key_values[key])
    #     if (cnt==100):
    #         return
    
    return key_values


def compare_dicts(true: dict, pred: dict) -> dict:
    """compare the error between two dicts

    Args:
        true (dict): truth
        pred (dict): prediction

    Returns:
        dict: relative error
    """
    res = []
    cnt=0
    for key in true:
        if key not in pred:
            pred[key]=0
            cnt+=1
        res.append(abs(((true[key]-pred[key])/true[key])))
        # print(key)
    # print(res)
    # plt.hist(res,bins=50)
    # plt.show()
    if cnt!=0:
        print("there are ", cnt, " missing values.")
    return res


def plot_count():
    """ plot count
    """
    mdn = read_results("mdn40/count1_ss1t_gg4.txt", split_char=",")
    truth = read_results("mdn40/count1truth.txt")
    kde = read_results("mdn40/count1gg10.txt")
    res0 = compare_dicts(truth, mdn)
    res1 = compare_dicts(truth, kde)
    res0 = [res * 100 for res in res0]
    res1 = [res * 100 for res in res1]
    plt.hist(res0, bins=50, color="r", alpha=0.2, label="MDN")
    plt.hist(res1, bins=50, color="b", alpha=0.6, label="ETRIML")
    plt.legend()
    plt.title("Histogram of relative error for COUNT")
    plt.ylabel("Frequency")
    plt.xlabel("Relative error")
    fmt = '%.2f%%'
    xticks = mtick.FormatStrFormatter(fmt)
    plt.gca().xaxis.set_major_formatter(xticks)
    # plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter())

    plt.text(10, 3, "MDN error " + str(sum(res0) / len(res0)) + "%")
    plt.text(10, 2, "ETRIML error " + str(sum(res1) / len(res1)) + "%")
    plt.show()


def plt501():
    """ plot for 501 group.
    """
    mdn = read_results("mdn501/sum1_ss1t_gg4.txt", split_char=",")
    truth = read_results("groundtruth/sum1.result")
    kde = read_results("ETRIML/sum1.txt")
    res0 = compare_dicts(truth, mdn)
    res1 = compare_dicts(truth, kde)
    res0 = [res * 100 for res in res0]
    res1 = [res * 100 for res in res1]
    plt.hist(res0, bins=50, color="r", alpha=0.2, label="MDN")
    plt.hist(res1, bins=50, color="b", alpha=0.6, label="ETRIML")
    plt.legend()
    plt.title("Histogram of relative error for COUNT")
    plt.ylabel("Frequency")
    plt.xlabel("Relative error")
    fmt = '%.2f%%'
    xticks = mtick.FormatStrFormatter(fmt)
    plt.gca().xaxis.set_major_formatter(xticks)
    # plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter())

    plt.text(10, 3, "MDN error " + str(sum(res0) / len(res0)) + "%")
    plt.text(10, 2, "ETRIML error " + str(sum(res1) / len(res1)) + "%")

    print("MDN error " + str(sum(res0) / len(res0)) + "%")
    print("ETRIML error " + str(sum(res1) / len(res1)) + "%")

    plt.show()


def plt_workload(agg_func="avg", suffix="_ss1t_gg4.txt", b_plot=True, b_merge_result_for_group=False, b_two_methods=False):
    mdn_errors = []
    kde_errors = []
    # prapare the files.
    for i in range(1, 11):
        prefix = agg_func+str(i)
        # print(prefix)
        truth = read_results(
            "experiments/results/groundtruth/1t2cols/"+prefix+".txt")
        # print("experiments/results/ETRIML/1t2cols/2_5g/" +
        #                    prefix+suffix)
        mdn = read_results("experiments/results/mdn/1t2cols/20g/" +
                           prefix+suffix, split_char=",")
        

        mdn_error = compare_dicts(truth, mdn)
        mdn_errors.append(mdn_error)
        if b_two_methods:
            kde = read_results(
                "experiments/results/deepdb/10g/"+prefix+".txt", split_char=",")
            kde_error = compare_dicts(truth, kde)
            kde_errors.append(kde_error)

    # mdn_errors = mdn_errors*100
    # if b_two_methods:
    #     kde_errors = kde_errors*100

    if b_plot:
        if b_merge_result_for_group:
            mdn_errors = np.array(mdn_errors)
            mdn_errors = np.mean(mdn_errors, axis=0)

            if b_two_methods:
                kde_errors = np.array(kde_errors)
                kde_errors = np.mean(kde_errors, axis=0)
        else:
            mdn_errors = np.array(list(chain.from_iterable(mdn_errors)))
            if b_two_methods:
                kde_errors = np.array(list(chain.from_iterable(kde_errors)))

        mdn_errors = mdn_errors*100
        if b_two_methods:
            kde_errors = kde_errors*100

        plt.hist(mdn_errors, bins=50, color="r", alpha=0.2, label="ETRIML-MDN")
        if b_two_methods:
            plt.hist(kde_errors, bins=50, color="b", alpha=0.6, label="ETRIML")
        plt.legend()
        plt.title("Histogram of relative error for " + agg_func.upper())
        plt.ylabel("Frequency")
        plt.xlabel("Relative error")
        fmt = '%.2f%%'
        xticks = mtick.FormatStrFormatter(fmt)
        plt.gca().xaxis.set_major_formatter(xticks)
        # plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter())

        plt.text(10, 150, "ETRIML-MDN error " +
                 "{0:.2f}".format(np.mean(mdn_errors)) + "%")
        if b_two_methods:
            plt.text(10, 180, "ETRIML error " +
                     "{0:.2f}".format(np.mean(kde_errors)) + "%")

        plt.show()
    print(agg_func)
    print("MDN error " + str(np.mean(mdn_errors)) + "%")
    if b_two_methods:
        print("ETRIML error " + str(np.mean(kde_errors)) + "%")
    if b_two_methods:
        return np.mean(mdn_errors), np.mean(kde_errors)
    else:
        return np.mean(mdn_errors)


def plt_501_bar_chart_error(suffix=".txt"):
    fontsize = 10
    mdn_count, kde_count = plt_workload(
        agg_func="count", suffix=suffix, b_plot=False)
    mdn_sum, kde_sum = plt_workload(
        agg_func="sum", suffix=suffix, b_plot=False)
    mdn_avg, kde_avg = plt_workload(
        agg_func="avg", suffix=suffix, b_plot=False)
    labels = ["COUNT", "SUM", "AVG", "OVERALL"]

    mdn = [mdn_count, mdn_sum, mdn_avg]
    kde = [kde_count, kde_sum, kde_avg]
    mdn.append(sum(mdn)/3.0)
    kde.append(sum(kde)/3.0)
    mdn = np.array(mdn)*100
    kde = np.array(kde)*100

    x_points = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    rect_mdn = ax.bar(x_points-width/2, mdn, width,
                      label="ETRIML-MDN", alpha=0.5)
    rect_kde = ax.bar(x_points+width/2, kde, width, label="ETRIML", alpha=0.8)
    ax.set_xticks(x_points)
    ax.set_xticklabels(labels)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
    ax.set_ylabel("Relative Error (%)", fontsize=fontsize)
    ax.set_xlabel("Aggregate function", fontsize=fontsize)
    ax.legend(loc="lower left", fontsize=fontsize)
    autolabel(rect_kde, ax)
    autolabel(rect_mdn, ax)

    # ax.set_ylim(0, 5)

    fig.tight_layout()
    plt.show()


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{0:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


if __name__ == "__main__":

    plt_workload(agg_func="count", suffix=".txt", b_plot=False,
                 b_merge_result_for_group=False, b_two_methods=False)
    plt_workload(agg_func="sum", suffix=".txt", b_plot=False,
                 b_merge_result_for_group=False, b_two_methods=False)
    plt_workload(agg_func="avg", suffix=".txt", b_plot=False,
                 b_merge_result_for_group=False, b_two_methods=False)