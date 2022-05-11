import numpy as np

# from etrimlclient.ml.mdn import KdeMdn, RegMdnGroupBy


def approx_integrate(func: callable, x_lb: float, x_ub: float, n_division=20) -> float:
    #print(">>> ml > integral.py > None : approx_integrate()")

    # simulate the integral using user-defined functions.

    # Args:
    #     func (callable): the integral funcion, must be able to predict for a list of points.
    #     x_lb (float): lower bound
    #     x_ub (float): upper bound
    #     n_division (int, optional): the mesh division number. Defaults to 20.

    # Returns:
    #     float: the approximate integral.
    grid, step = np.linspace(x_lb, x_ub, n_division, retstep=True)
    # print(grid)
    # print(step)
    # print(func(grid)[0:-1].sum()*step)
    # print(func(grid)[1:].sum()*step)
    predictions = func(grid)
    return (0.5*(predictions[0]+predictions[-1]) + predictions[1:-1])*step
    # return (func(grid)[0:-1].sum() + func(grid)[1:].sum())*0.5*step


def prepare_reg_density_data(density, x_lb: float, x_ub: float, groups: list, reg,  runtime_config):
    #print(">>> ml > integral.py > None : prepare_reg_density_data()")

    # prepare_reg_density_data(density: KdeMdn, x_lb: float, x_ub: float, groups: list, reg: RegMdnGroupBy = None,  n_division: int = 20):
    n_division = runtime_config["n_division"]
    x_points, step = np.linspace(x_lb, x_ub, n_division, retstep=True)

    # print("groups in prepare integral----------", groups)
    # raise

    reg_x_points = list(x_points)*len(groups)
    try:  # group key is [g1-g2]
        reg_g_points = [g.split(",")
                        for g in groups for _ in range(n_division)]
        density_g_points = [i.split(",") for i in groups]
    except AttributeError:  # group key is [g1,g2]
        reg_g_points = [list(g) for g in groups for _ in range(n_division)]
        density_g_points = [list(i) for i in groups]

    # print(density_g_points)
    density_x_points = list(x_points)

    # print(density_g_points)
    # print(density_x_points)

    pre_density = density.predict(
        density_g_points, density_x_points, runtime_config, b_plot=False)

    pre_reg = None if reg is None else reg.predict(
        reg_g_points, reg_x_points, runtime_config)
    if pre_reg is not None:
        pre_reg = np.array(pre_reg).reshape(len(groups), n_division)

    return pre_density, pre_reg, step


def prepare_var(density, groups, runtime_config):
    #print(">>> ml > integral.py > None : prepare_var()")

    print("groups", groups)

    return density.var(groups, runtime_config) #{"group":99999.99}


def approx_count(pred_density, step: float):
    #print(">>> ml > integral.py > None : approx_count()")

    #  the integral only use the left point in the interval, not the central point, need improvement
    # return np.sum(pred_density[:, :-1], axis=1)*step
    result = np.sum(pred_density[:, 1:-1], axis=1)
    result = np.add(result, pred_density[:, 0]*0.5)
    result = np.add(result, pred_density[:, -1]*0.5)
    return result*step


def approx_sum(pred_density, pre_reg, step: float):
    #print(">>> ml > integral.py > None : approx_sum()")

    multi = np.multiply(pred_density, pre_reg)
    # result = np.sum(multi[:, :-1], axis=1)
    result = np.sum(multi[:, 1:-1], axis=1)
    result = np.add(result, multi[:, 0]*0.5)
    result = np.add(result, multi[:, -1]*0.5)

    return result*step


def approx_avg(pred_density, pre_reg, step: float):
    #print(">>> ml > integral.py > None : approx_avg()")

    results = np.divide(approx_sum(pred_density, pre_reg,
                                   step), approx_count(pred_density, step))
    return results


def sin_(points: list) -> float:
    #print(">>> ml > integral.py > None : approx_sin()")
   
    return np.sin(points)
    

if __name__ == "__main__":
    print(approx_integrate(sin_, 0, 3.1415926, 200))