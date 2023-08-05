__author__ = "Thomas Baldauf"
__email__ = "thomas.baldauf@dlr.de"
__license__ = "MIT"
__birthdate__ = '06.10.2022'
__status__ = 'dev' # options are: dev, test, prod

from sfctools.examples.example_wrapper import Example

from sfctools.datastructs.inventory import Inventory
from sfctools import Agent

def run():
    class InventoryAgent(Agent): # basic agent with an inventory
        def __init__(self):
            super().__init__()
            self.inventory = Inventory(self)

    # perform some arbitrary manipulations on the inventory
    my_agent = InventoryAgent()
    my_agent.inventory.add_item("Apple",1,3.0)
    my_agent.inventory.add_item("Apple",1,5.0)
    my_agent.inventory.remove_item("Apple", 1)
    w = my_agent.inventory.worth
    my_agent.inventory.add_item("Pear",2,2.0)
    my_agent.inventory.remove_item("Pear", 2)

    n_a = my_agent.inventory.get_inventory("Apple")
    n_p = my_agent.inventory.get_inventory("Pear")
    w2 = my_agent.inventory.worth

    print("n_a",n_a)
    print("n_p",n_p)
    print("w2",w2)


class InventoryExample(Example):
    def __init__(self):
        super().__init__(run)
