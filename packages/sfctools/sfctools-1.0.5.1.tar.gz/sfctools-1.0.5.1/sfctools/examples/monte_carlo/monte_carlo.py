from sfctools.automation.runner import ModelRunner
import numpy as np
import pandas as pd


"""
This tests the automation routines for monte-carlo batches
"""

from sfctools.examples.example_wrapper import Example



def run():
    # run this in the upper directory via pytest tests/, otherwise this will fail
    settings_path =  "sfctools/examples/monte_carlo/testsettings.yml"
    results_path = "sfctools/examples/monte_carlo/result/"

    def builder():
        # placeholder for agent builder,
        # do nothing here
        return None

    def iter(n): # one model iteration, repeated n times
        vals = []
        for i in range(n):
            vals.append(np.random.rand())

        return pd.DataFrame({"Value":vals}) # has to return a dataframe

    # create model runner
    mr = ModelRunner(settings_path,results_path,builder,iter)
    mr.run(10,20)


class MonteCarloExample(Example):
    def __init__(self):
        super().__init__(run)
