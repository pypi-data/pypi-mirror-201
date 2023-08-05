__author__ = "Thomas Baldauf"
__email__ = "thomas.baldauf@dlr.de"
__license__ = "MIT"
__birthdate__ = '06.10.2022'
__status__ = 'dev' # options are: dev, test, prod

from sfctools.examples.example_wrapper import Example


def run():

    from sfctools import Agent , BalanceEntry

    class MyAgent(Agent):

        def __init__(self):

            super().__init__()

            with self.balance_sheet.modify:
                self.balance_sheet.change_item("Cash", BalanceEntry.ASSETS, 10.0)
                self.balance_sheet.change_item("Equity", BalanceEntry.EQUITY, 10.0)

            print("Hello Agent")


    my_agent = MyAgent()

    print(my_agent.balance_sheet.to_string())



class HelloWorldExample(Example):
    def __init__(self):
        super().__init__(run)
