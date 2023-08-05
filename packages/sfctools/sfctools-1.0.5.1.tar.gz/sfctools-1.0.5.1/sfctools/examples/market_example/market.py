__author__ = "Thomas Baldauf"
__email__ = "thomas.baldauf@dlr.de"
__license__ = "MIT"
__birthdate__ = '06.10.2022'
__status__ = 'dev' # options are: dev, test, prod


from sfctools import MarketMatching, Agent
import numpy as np
from sfctools.examples.example_wrapper import Example


def run(show_plot=True):
    # define a rudimentary trader class

    class Trader(Agent):
        # a rudimentary trader
        def __init__(self):
            super().__init__()

    supply_traders = [Trader() for i in range(50)]
    demand_traders = [Trader() for i in range(22)] # generate some agents

    # define a market and a matching rule

    class Market(MarketMatching):
        """
        My market for matching supply and demand
        """
        def __init__(self):
            super().__init__()

        def rematch(self):
            # match the suppliers and demanders at random

            for i in self.demand_list:
                for j in self.supply_list:
                    u = np.random.rand()
                    if u > 0.3:
                        self.link_agents(j,i,u)


    # generate a market and add the traders
    my_market = Market()
    [my_market.add_demander(agent) for agent in demand_traders]
    [my_market.add_supplier(agent) for agent in supply_traders]

    # re-match the market traders
    my_market.rematch()

    # plot the resulting network
    if show_plot:
        my_market.plot()

    # print suppliers of demander 0
    print(my_market.get_suppliers_of(demand_traders[0]))


class MarketExample(Example):
    def __init__(self):
        super().__init__(lambda: run(show_plot=False))


if __name__ == "__main__":
    my_instance = MarketExample()
    my_instance.run()
