import poc_simpletest
import poc_clicker_provided as provided


TESTSUITE = poc_simpletest.TestSuite()
BuildInfo = provided.BuildInfo()
SIM_TIME = 10000000000.0


def phase_one_tests(ClickerState):
    test = ClickerState()

    # Initialization
    TESTSUITE.run_test(str(test.get_cookies()), "0.0", "Test 1: Initial amount of cookies should be equal 0.0")
    TESTSUITE.run_test(str(test.get_time()), "0.0", "Test 2: Initial time should be equal 0.0")
    TESTSUITE.run_test(str(test.get_cps()), "1.0", "Test 3: Initial CPS should be equal 1.0")
    TESTSUITE.run_test(str(test.get_history()), "[(0.0, None, 0.0, 0.0)]", "Test 4: Initial history should be [(0.0, None, 0.0, 0.0)]")
    TESTSUITE.run_test(str(test.time_until(5.1)), "6.0", "Test 5: time_until should return float without fractional part")
    TESTSUITE.run_test(str(test.time_until(0.0)), "0.0", "Test 6: time_until should return 0.0 if given amount of cookies <= current cookies")

    test.wait(5)
    TESTSUITE.run_test(str(test.get_cookies()), "5.0", "Test 7: wait(5) should increase current cookies by 5.0")
    TESTSUITE.run_test(str(test.get_time()), "5.0", "Test 8: wait(5) should increase time by 5.0")
    TESTSUITE.run_test("%0.1f, %0.1f" %(test.time_until(4.0), test.time_until(5.0)), "0.0, 0.0", "Test 9: time_until(n) for n <= current cookies should return 0.0")

    test.wait(0)
    test.wait(-1)
    TESTSUITE.run_test(str(test.get_time()), "5.0", "Test 10: wait(n) should do nothing if n <= 0")
    TESTSUITE.run_test(str(test.get_history())=="[(0.0, None, 0.0, 0.0)]", True, "Test 11: wait() should not change history")

    test.buy_item("item", 5, 1)
    TESTSUITE.run_test("%0.1f, %0.1f" %(test.get_cookies(), test.get_cps()), "0.0, 2.0","Test 12: Current cookies and CPS should be updated")
    TESTSUITE.run_test(str(test.get_history()[-1]), "(5.0, 'item', 5, 5.0)", "Test 13: history should be updated")

    test.buy_item("item", 5, 1)
    TESTSUITE.run_test("%0.1f, %0.1f" %(test.get_cookies(), test.get_cps()), "0.0, 2.0","Test 14: buy_item() should do nothing if cost > current cookies")


def phase_two_tests(simulate_clicker, strategy_cursor):
    try:
        test = simulate_clicker(BuildInfo, 5.0, lambda *args: None)
    except KeyError:
        print("You are trying to call some of BuildInfo methods inside of simulate_clicker with None as item")
        return
    TESTSUITE.run_test(str(test.get_history()), "[(0.0, None, 0.0, 0.0)]", "Test 15: strategy_none should not change history")
    TESTSUITE.run_test(str(test.get_cookies()), "5.0", "Test 16: strategy_none should generate t cookies in t time")

    test = simulate_clicker(BuildInfo, SIM_TIME, strategy_cursor)
    TESTSUITE.run_test("%11.1f, %11.1f, %0.1f" %(test.get_time(),test.get_cookies(), test.get_cps()),\
                       "10000000000.0, 6965195661.5, 16.1", "Test 17: strategy_cursor doesn't work as expected")
    
    test = simulate_clicker(BuildInfo, 15.0, strategy_cursor)
    TESTSUITE.run_test("%0.1f, %0.1f, %0.1f" %(test.get_time(), test.get_cookies(), test.get_cps()),\
                       "15.0, 0.0, 1.1", "Test 18: simulate_clicker should buy item if sim time == item cost")


def phase_three_tests(simulate_clicker,strategy_cursor, strategy_cheap, strategy_expensive, strategy_best):
    test = simulate_clicker(provided.BuildInfo(growth_factor=10), 150.0, strategy_cheap)
    TESTSUITE.run_test(test.get_history()[-1][1]=="Grandma", True, "Test 19: strategy_cheap doesn't select the cheapest item")
    TESTSUITE.run_test(strategy_cheap(0, 1, 10, BuildInfo)==None, True, "Test 20: strategy_cheap should return None if you can't afford any item in time left")
    TESTSUITE.run_test(strategy_cheap(15.0, 0.0, 0.0, BuildInfo)=="Cursor", True, "Test 21: strategy_cheap: probably you forgot to add cookies to your budget")


    test = simulate_clicker(BuildInfo, 100.0, strategy_expensive)
    TESTSUITE.run_test(test.get_history()[-1][1]=="Grandma", True, "Test 22: strategy_expensive doesn't select the most expensive item that you can get")
    TESTSUITE.run_test(strategy_expensive(0, 1, 10, BuildInfo)==None, True, "Test 23: strategy_expensive should return None if you can't afford any item in given time")
    TESTSUITE.run_test(strategy_expensive(100.0, 1.0, 15.0, BuildInfo)=="Grandma", True, "Test 24: strategy_expensive: probably you forgot to add cookies to your budget" )
    


def run_tests(ClickerState, simulate_clicker=None, strategy_cursor=None, strategy_cheap=None, strategy_expensive=None, strategy_best=None):
    phase_one_tests(ClickerState)
    if simulate_clicker != None:
        phase_two_tests(simulate_clicker,  strategy_cursor)
        if strategy_cheap != None:
            phase_three_tests(simulate_clicker, strategy_cursor, strategy_cheap, strategy_expensive, strategy_best)
    TESTSUITE.report_results()


