
from attune.src.qtattune import run_app
import subprocess

import sys
import os


class Gui:
    """
    The attune-gui for usage within Python
    """

    def __init__(self):
        pass

    def run(self):
        # runs the attune gui within Python

        run_app()


def run_gui():
    g = Gui()
    g.run()


if __name__ == "__main__":
    run_gui()
