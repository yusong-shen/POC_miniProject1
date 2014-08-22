"""
Simulator for resource generation with upgrades
"""

import simpleplot
import math
import codeskulptor
codeskulptor.set_timeout(20)


def resources_vs_time(upgrade_cost_increment, num_upgrade):
    """
    Build function that performs unit upgrades with specified cost increments
    """
    # upg_cost_inc = 0.5 , num_upg = 20
    # [current_time , total_res]->[1.0, 1] ->[1.75 ,2.5] ->[2.42 ,4.5]
    result = []
    total_res = 0.0 
    res_rate = 1.0 # initial resource generating rate = 1 unit/s
    upg_cost = 1.0 # initial upgrade cost = 1 unit/s
    cur_time = 0.0 # by second
    last_upg_time = 0.0
    # upgrade once in each iteration
    for i in range(num_upgrade):
        # print "total_res, res_rate, cur_time, upg_cost"
        # print total_res,res_rate,cur_time,upg_cost
        last_upg_time = cur_time
        cur_time += upg_cost/res_rate # update the cur_time
        total_res += res_rate*(cur_time-last_upg_time)
        # upgrate : 1) increse the upg_cost 2)increse the res_rate
        upg_cost += upgrade_cost_increment
        res_rate += 1
        result.append([cur_time, total_res])
    return result

def test():
    """
    Testing code for resources_vs_time
    """
    data1 = resources_vs_time(0.0, 50)
    data2 = resources_vs_time(0.5, 40)
    data3 = resources_vs_time(1.0, 30)
    data4 = resources_vs_time(2.0, 20)
    # print data1
    # print data2
    simpleplot.plot_lines("Growth", 600, 600, "time", "total resources", [data1, data2, data3, data4])

test()


# Sample output from the print statements for data1 and data2
#[[1.0, 1], [1.75, 2.5], [2.41666666667, 4.5], [3.04166666667, 7.0], [3.64166666667, 10.0],...
# [4.225, 13.5], [4.79642857143, 17.5], [5.35892857143, 22.0], [5.91448412698, 27.0], [6.46448412698, 32.5],...
# [7.00993867244, 38.5], [7.55160533911, 45.0], [8.09006687757, 52.0], [8.62578116328, 59.5],...
# [9.15911449661, 67.5], [9.69036449661, 76.0], [10.2197762613, 85.0], [10.7475540391, 94.5], ...
# [11.2738698286, 104.5], [11.7988698286, 115.0]]

#[[1.0, 1], [2.25, 3.5], [3.58333333333, 7.5], [4.95833333333, 13.0], [6.35833333333, 20.0], ...
# [7.775, 28.5], [9.20357142857, 38.5], [10.6410714286, 50.0], [12.085515873, 63.0], [13.535515873, 77.5]]

