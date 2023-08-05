__author__ = "Thomas Baldauf"
__email__ = "thomas.baldauf@dlr.de"
__license__ = "MIT"
__birthdate__ = '06.10.2022'
__status__ = 'dev' # options are: dev, test, prod

from sfctools.examples.example_wrapper import Example

from sfctools.datastructs.bank_order_book import BankOrderBook
from sfctools.bottomup.matching import MarketMatching
from sfctools import Agent
import matplotlib.pyplot as plt


def run():

    # create a bank agent
    class Bank(Agent):
        def __init__(self):
            super().__init__()

    class MyCreditMarket(MarketMatching):
        def __init__(self):
            super().__init__()

        def rematch(self):
            # link some agents

            r_l = 0.05 # interest on loans

            self.link_agents(self.supply_list[0],self.demand_list[1],r_l)
            self.link_agents(self.supply_list[0],self.demand_list[5],r_l)
            self.link_agents(self.supply_list[3],self.demand_list[5],r_l)

            new_loans = 4.2 # quantity
            duration = 5    # 5 periods duration

            for bank in [self.supply_list[0],self.supply_list[3]]:
                for creditor in [self.demand_list[1],self.demand_list[5]]:
                    bank.order_book.add_loans(creditor,new_loans,r_l,t=duration)

    class MyDepositMarket(MarketMatching):
        def __init__(self):
            super().__init__()

        def rematch(self):
            # link some agents

            r_d = 0.03 # interest on deposits all same

            self.link_agents(self.supply_list[2],self.demand_list[3],r_d)
            self.link_agents(self.supply_list[2],self.demand_list[6],r_d)
            self.link_agents(self.supply_list[4],self.demand_list[6],r_d)

            new_deposits = 1000.0 # quantity of deposits all the same

            # add deposits at banks
            for bank in [self.demand_list[3], self.demand_list[6]]:
                for depositor in [self.supply_list[2],self.supply_list[4]]:
                    bank.order_book.add_deposits(depositor,new_deposits, r_d)

    # create some agents
    firms = [Agent() for i in range(12)] # create some firms seeking for creidt
    depositors = [Agent() for i in range(25)] # create some depositors
    banks = [Bank() for i in  range(10)] # create banks

    # create markets
    credit_market = MyCreditMarket()
    deposit_market = MyDepositMarket()

    # register agents at markets
    for f in firms:
        credit_market.add_demander(f)

    for d in depositors:
        deposit_market.add_supplier(d)

    for b in banks:
        credit_market.add_supplier(b)
        deposit_market.add_demander(b)

    for b in banks: # add order book to banks
        b.order_book = BankOrderBook(b,credit_market,deposit_market)

    # match the markets
    deposit_market.rematch()
    credit_market.rematch()

    # look at some output
    df_depos,df_loans = banks[3].order_book.to_dataframe()

    print(df_depos["Agent"])

    loans = banks[3].order_book.get_loans_of(firms[5])

    # process the loan
    loans[0]["Time"] += 1
    t_remain = loans[0]["Maturity"] - loans[0]["Time"]

    # check in original data
    df_depos,df_loans = banks[3].order_book.to_dataframe()

    print(df_loans["Time"])


class BankOrderBookExample(Example):
    def __init__(self):
        super().__init__(run)
