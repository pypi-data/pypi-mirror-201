
"""
__author__ Thomas Badauf, Ve
__date__ March 2023

This is a wrapper class to run an example instance.
"""

import time

class Example():
    """
    This is a wrapper class to run an example instance.
    """

    def __init__(self,runner_method):
        """
        :param runner_method: a method to execute in this example
        """
        self.runner_method = runner_method
        self.t_start = None
        self.t_end = None
        self.rtime = None
        self.res = None

    def run(self,verbose=True):
        """
        run the actual example
        """
        self.t_start = time.time()
        self.res = self.runner_method()
        self.t_end = time.time()

        try:
            self.rtime = self.t_end - self.t_start
        except:
            pass

        if verbose:
            self.print_stats()

        return self.res


    def print_stats(self):
        """
        print some statistics,
        """

        if self.t_start is None or self.t_end is None:
            print("< No stats available. > ")
        
        statstr = """
        STATS FOR %s
        -----------------------------
          runtime:  %.2f
          result type: %s
        -----------------------------
        """  % (self.__class__.__name__,self.rtime,type(self.res))

        print(statstr)
