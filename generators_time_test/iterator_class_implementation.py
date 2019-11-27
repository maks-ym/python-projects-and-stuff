from utils import *

# Iterator for next power of two.
class NextPowTwo:
    def __init__(self, max_ele = 0):
        self.max_ele = max_ele

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n <= self.max_ele:
            result = 2 ** self.n
            self.n += 1
            return result
        else:
            raise StopIteration


# Improved iterator for next power of two
class NextPowTwoImproved:
    def __init__(self, max_ele = 0):
        self.max_ele = max_ele

    def __iter__(self):
        self.n = 0
        self.result = 1
        return self

    def __next__(self):
        if self.n <= self.max_ele:
            result = self.result
            self.result *= 2
            self.n += 1
            return result
        else:
            raise StopIteration


def NextPowTwoTimeTest(func_to_test=NextPowTwo, max_ele=0, print_log=False):
    tot_time = time.time()
    times_arr = []
    it = iter(func_to_test(max_ele=max_ele))

    @timeit
    def measured_iter(it):
        return next(it)

    for i in range(max_ele):
        c_time, c_res, c_func = measured_iter(it)
        times_arr.append(c_time)
        if print_log:
            print(f"{c_time}, {c_res}, {c_func}")
    tot_time = time.time() - tot_time

    return times_arr, tot_time


if __name__ == '__main__':
    test_funcs = [NextPowTwo, NextPowTwoImproved]
    max_val = 500000
    result_tot_times = {}
    res_time_arrays = {}

    for test_func in test_funcs:
        cur_time_arr, cur_tot_time = NextPowTwoTimeTest(test_func, max_ele=max_val, print_log=False)
        result_tot_times[test_func.__name__] = cur_tot_time
        res_time_arrays[test_func.__name__] = cur_time_arr

    for k, v in result_tot_times.items():
        print(f"{k}: {v} s")

    create_figure(res_time_arrays)
    