__author__ = "Thomas Baldauf"
__email__ = "thomas.baldauf@dlr.de"
__license__ = "MIT"
__birthdate__ = '06.10.2022'
__status__ = 'dev' # options are: dev, test, prod

from sfctools.examples.example_wrapper import Example

from sfctools import Clock
import datetime
from dateutil.relativedelta import relativedelta

def run():
    t0 = datetime.datetime(2020, 1, 1) # set up initial time

    clock = Clock(t0=t0, dt=relativedelta(years=1)) # setup a clock
    t0 = clock.get_time() # get the starting time

    [clock.tick() for i in range(5)] # tick 5 times

    t1 = clock.get_time()        # get the integer time
    t2 = clock.get_real_time()   # get the actual datetime time

    clock.reset() # reset clock to zero

    t3 = clock.get_time()
    t4 = clock.get_real_time()

    print("t0:",t0)
    print("t1:",t1)
    print("t2:",t2)
    print("t3:",t3)
    print("t4:",t4)

class ClockExample(Example):
    def __init__(self):
        super().__init__(run)

if __name__ == "__main__":
    my_instance = ClockExample()
    my_instance.run()
