__author__ = "Thomas Baldauf"
__email__ = "thomas.baldauf@dlr.de"
__license__ = "MIT"
__birthdate__ = '06.10.2022'
__status__ = 'dev' # options are: dev, test, prod

from sfctools.examples.example_wrapper import Example

from sfctools.datastructs.signalslot import Signal,Slot
from sfctools.datastructs.signalslot import SignalSlot
from sfctools import Agent

def run():

    class Sender(Agent): # a dummy receiver
        def __init__(self):
            super().__init__()
            self.message = None


    class Receiver(Agent): # a dummy sender
        def __init__(self):
            super().__init__()
            self.recording = None

    # create two dummy agents
    my_sender = Sender()
    my_receiver = Receiver()
    my_other_receiver = Receiver()

    # create signals and slots
    sender_signal = Signal("Message")
    receiver_slot = Slot("Message")
    sender_signal.connect_to([receiver_slot])

    # link signals and slots to agents
    my_sender.message = sender_signal
    my_receiver.recording = receiver_slot
    my_other_receiver.recording = receiver_slot

    # emit signal
    sender_signal.update("Secret Message")
    sender_signal.emit(verbose=True)

    # read recording
    print("received:", my_receiver.recording.value())
    print("received (other):", my_other_receiver.recording.value())


class SignalSlotExample(Example):
    def __init__(self):
        super().__init__(run)
