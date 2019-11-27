import time
import matplotlib.pyplot as plt

def timeit(func):
    def wrapper(*args, **kw):
        res_time = time.time()
        func_res = func(*args, **kw)
        res_time = time.time() - res_time
        return res_time, func_res, func.__name__
    return wrapper


def create_subplot(place, x, y, title="Figure"):
    plt.subplot(place)
    plt.plot(x, y)
    plt.title(title)


def create_figure(dict_xy):
    plt.figure()
    for i, (k, v) in enumerate(dict_xy.items()):
        p = "12" + str(i+1)
        print(p)
        create_subplot(p, list(range(len(v))), v, k)
    plt.show()