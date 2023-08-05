__author__ = "Thomas Baldauf"
__email__ = "thomas.baldauf@dlr.de"
__license__ = "MIT"
__birthdate__ = '06.10.2022'
__status__ = 'dev' # options are: dev, test, prod

from sfctools.examples.example_wrapper import Example


from .agents.household import Household
from .agents.production import Production
from .agents.government import Government

from sfctools import Clock, FlowMatrix, Settings, World
from sfctools.misc.mpl_plotting import matplotlib_lineplot, matplotlib_barplot
from sfctools import IndicatorReport, ReportingSheet, BalanceSheet

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def run(show_plot=True):

    FlowMatrix().reset()
    World().reset()


    # read settings
    Settings().read_from_yaml("sfctools/examples/exampleabm/settings.yml")

    # generate agents
    my_household  = Household()
    my_production = Production()
    my_government = Government()

    # link the agents
    my_household.link()
    my_production.link()
    my_government.link()

    # simulation duration
    T = int(Settings().get_hyperparameter("T")) # simulation length
    T_burn_in = int(Settings().get_hyperparameter("T_burn")) # simulation length

    # prepare output data
    rs = ReportingSheet([
        IndicatorReport("Time","C"),
        IndicatorReport("Time","G"),
        IndicatorReport("Time","Y"),
        IndicatorReport("Time","T"),
        IndicatorReport("Time","DI")])

    household_balance_data = []  # logs the household balance sheets
    governmnt_balance_data = []  # logs the government balance sheets

    # simulation loop
    for i in range(T):

        # reset flow matrix
        FlowMatrix().reset()

        # update all agents individually
        my_household.update()
        my_government.update()
        my_production.update()

        Clock().tick() # increase clock by one tick

        # output data
        if i > T_burn_in: # after burn-in

            IndicatorReport.getitem("C").add_data(my_household.C)
            IndicatorReport.getitem("G").add_data(my_government.G)
            IndicatorReport.getitem("Y").add_data(my_production.Y)
            IndicatorReport.getitem("T").add_data(my_production.T)
            IndicatorReport.getitem("DI").add_data(my_household.DI)

            # plot agent's balance sheets
            household_balance_data.append(my_household.balance_sheet.raw_data)
            governmnt_balance_data.append(my_government.balance_sheet.raw_data)

        # reset agents
        my_household.reset()
        my_production.reset()
        my_government.reset()

    # print flow matrix
    print(FlowMatrix().to_string())

    if show_plot:
        fig = FlowMatrix().plot_sankey(show_values=True,show_plot=False)
        plt.savefig("sfctools/examples/exampleabm/figures/sankey.png")
        plt.close()

        fig = FlowMatrix().plot_colored(show_plot=False)
        plt.savefig("sfctools/examples/exampleabm/figures/matrix.png")
        plt.close()

        # plot output indicators
        fig = rs.plot(show_plot=False)
        plt.savefig("sfctools/examples/exampleabm/figures/outputs.png")
        plt.close()

        # plot the stocks of government and household
        # BalanceSheet.plot_list(household_balance_data, dt=5, xlabel="Time", title="Household",  show_liabilities=False)
        BalanceSheet.plot_list(governmnt_balance_data, dt=5, xlabel="Time", title="Example", show_liabilities=True)


class ABMExample(Example):
    def __init__(self):
        super().__init__(lambda: run(show_plot=False))


if __name__ == "__main__":
    my_instance = ABMExample()
    my_instance.run()
