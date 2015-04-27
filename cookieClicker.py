"""
Cookie Clicker Simulator
"""
try:
    import simpleplot

except ImportError:
    import SimpleGUICS2Pygame.simpleplot as simpleplot

import math

# Used to increase the timeout, if necessary
# import codeskulptor
# codeskulptor.set_timeout(20)

import poc_clicker_provided as provided
# Build_info class
# contains the information of items


# Constants
# 10^10
SIM_TIME = 10000000000.0
# 10^4 for debug
# SIM_TIME = 10000.0
class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._tot_cookies = 0.0
        self._cur_cookies = 0.0
        self._cur_time = 0.0
        self._cps = 1.0
        # each history state has form like
        # (time, item, cost of item, total cookies)
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """

        return "_tot_cookies:%f, _cur_cookies:%f, \n_cur_time:%f, CPS:%f, \nlast_item:%s"%(
                self._tot_cookies,self._cur_cookies,self._cur_time,self._cps,self.get_history()[-1][1])
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cur_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._cur_time

    def get_tot_cookies(self):
        """
        Get the total number of cookies

        Helper function added by myself
        """
        return self._tot_cookies

    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self.get_cookies() >= cookies:
            return 0.0
        else:
            cookies_gap = cookies - self.get_cookies()
            # gap: 9.24 --> 10, 9.0 --> 9
            return float(math.ceil(cookies_gap/self.get_cps()))
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            # wait for given amount of time?
            # update state
            self._cur_time += time
            self._cur_cookies += time*self._cps
            self._tot_cookies += time*self._cps
        else:
            pass
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self.get_cookies() >= cost:
            state = (self.get_time(), item_name, cost, self.get_tot_cookies())
            self._history.append(state)

            # update the current cookies account
            # and the current cookies per second
            self._cur_cookies -= cost
            self._cps += additional_cps
        else:
            pass
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """

    # make a clone to the build_info object
    build_info = build_info.clone()

    # create a new ClickState object
    clickstate = ClickerState()
    while(clickstate.get_time() <= duration):
        # compute some basic parameters
        cookies = clickstate.get_cookies()
        cps = clickstate.get_cps()
        time_left = duration - clickstate.get_time()
        # pick an item according to the given strategy
        item  = strategy(cookies, cps, time_left, build_info)

        # if the item is None, which means that no more item will
        # be purchased, then break out of the loop
        if item == None:
            break

        # determine how much time  must elapse until is possible to 
        # purchase the item. if you have to wait past the duration,
        # you should end the simulation
        cost = build_info.get_cost(item)
        wait_time = clickstate.time_until(cost)
        if wait_time > time_left :
            break

        # wait until that time
        clickstate.wait(wait_time)

        # buy the item
        additional_cps = build_info.get_cps(item)
        clickstate.buy_item(item, cost, additional_cps)

        # print "cookies, cps, time_left, item, cost, wait_time"    
        # print cookies, cps, time_left, item, cost, wait_time

        # update the build information
        build_info.update_item(item)

    # if there is time left , still allow the cookies to accumulate 
    time_left = duration - clickstate.get_time()
    clickstate.wait(time_left)

    # allow to buy the multiple items at the final time

    return clickstate


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    if cookies+cps*time_left >= build_info.get_cost("Cursor"):
        return "Cursor"
    else:
        return None

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Always select the cheapest item that you can afford 
    in the given time_left

    """
    min_cost = float("inf")
    # return None if we can afford nothing
    cheapest_item = None
    items_list = build_info.build_items()
    for item in items_list:
        cost = build_info.get_cost(item)
        # check if we can afford this item in given time left
        if cookies+cps*time_left >= build_info.get_cost(item):
            if cost < min_cost:
                min_cost = cost
                cheapest_item = item

    return cheapest_item

def strategy_expensive(cookies, cps, time_left, build_info):
    """ 
    Always select the most Expensive item that you can afford
    in the given time_left
    6.8e+17
    """
    max_cost = 0
    most_expensive_item = None
    items_list = build_info.build_items()
    for item in items_list:
        cost = build_info.get_cost(item)
        # check if we can afford this item in given time left
        if cookies+cps*time_left >= build_info.get_cost(item):
            if cost > max_cost:
                max_cost = cost
                most_expensive_item = item        

    return most_expensive_item

def strategy_best1(cookies, cps, time_left, build_info):
    """ 
    The best strategy 1 -- strategy_expensive_pro1
    1.22e+18

    """
    max_cost = 0
    most_expensive_item = None
    items_list = build_info.build_items()
    for item in items_list:
        cost = build_info.get_cost(item)
        # check if we can afford this item in given time left
        if cookies+cps*time_left*0.1 >= cost:
            if cost > max_cost:
                max_cost = cost
                most_expensive_item = item


    return most_expensive_item

def strategy_best(cookies, cps, time_left, build_info):
    """ 
    The best strategy2

    Always select the most efficient one
    by efficient I mean :  additional_cps/item_cost 
    """

    # the less anti_efficiency, the better the item
    most_efficient_item = None 
    min_anti_efficiency = float("inf")
    items_list = build_info.build_items()
    for item in items_list:
        cost = build_info.get_cost(item)
        additional_cps = build_info.get_cps(item) 
        anti_efficiency = cost/additional_cps
        if cookies+cps*time_left >= cost:
            if anti_efficiency < min_anti_efficiency:
                min_anti_efficiency = anti_efficiency
                most_efficient_item = item

    return most_efficient_item

def strategy_best3(cookies, cps, time_left, build_info):
    """ 
    The best strategy3

    Always select the most efficient one
    by efficient I mean :  additional_cps/item_cost*a_adjusting_factor 
    """

    # the less anti_efficiency, the better the item
    most_efficient_item = None 
    min_anti_efficiency = float("inf")
    items_list = build_info.build_items()
    for item in items_list:
        cost = build_info.get_cost(item)
        additional_cps = build_info.get_cps(item) 
        anti_efficiency = 2*cost/additional_cps
        if cookies+cps*time_left >= cost:
            if anti_efficiency < min_anti_efficiency:
                min_anti_efficiency = anti_efficiency
                most_efficient_item = item

    return most_efficient_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    # run_strategy("Cursor", SIM_TIME, strategy_cursor)
    # run_strategy("None", SIM_TIME, strategy_none)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best1", SIM_TIME, strategy_best1)
    run_strategy("Best2", SIM_TIME, strategy_best)
    run_strategy("Best3", SIM_TIME, strategy_best3)
    
run()
    
# # testing __init__ , __str__, get_cookies,
# # get_cps, get_time, get_history
# import user34_1yyodNweJj_0 as init_test
# init_test.run_test(ClickerState)

# #  testing wait: (you need to pass first test)
# import user34_gwOBYcB0vg_5 as wait_test
# wait_test.run_test(ClickerState)

# # testing time_until: (you need to pass test 1 and 2)
# import user34_JegqHUeyeq_1 as time_until_test
# time_until_test.run_test(ClickerState)

# # testing buy_item: (you need to pass test 1 and 2)
# import user34_CX25TCXsrD_4 as buy_test
# buy_test.run_test(ClickerState)

# # for running all tests
# import user34_muNP84fR8e_2 as testsuite
# testsuite.run_tests(ClickerState,simulate_clicker,
#     strategy_cursor, strategy_cheap, strategy_expensive, 
#     strategy_best)

# # Patrick Seeber's test suite 
# # note that this test suite assumes that you have implemented strategy_none
# import user34_GhjnBEJSmI_10 as test_suite
# test_suite.run_simulate_clicker_tests(simulate_clicker,strategy_none,strategy_cursor)
# # test_suite.run_clicker_state_tests(ClickerState)

