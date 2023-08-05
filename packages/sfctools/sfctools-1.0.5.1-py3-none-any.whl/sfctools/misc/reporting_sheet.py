__version__ = "0.3"
__author__ = "Thomas Baldauf"
__email__ = "thomas.baldauf@dlr.de"
__license__ = "MIT"
__birthdate__ = '15.11.2021'
__status__ = 'dev' # options are: dev, test, prod

import pandas as pd
import numpy as np
import warnings

"""
This file embraces the following features

IndicatorReport
DistributionReport
ReportingSheet

WARNING BETA, under development, use at own risk!
"""

class IndicatorReport:
    """
    A generic class for logging scalar values ('indicators').
    """

    _instances = {}

    def __init__(self,xlabel,ylabel,data=None):
        """
        :param xlabel: x axis label, str
        :param ylabel: y axis label, str
        :param data: some initial data (default None). Has to have 'append' method
        """
        if data is not None:
            self.data = data
        else:
            self.data = []
        self.xlabel = xlabel
        self.ylabel = ylabel

        if not self.ylabel in self.__class__._instances:
            self.__class__._instances[self.ylabel] = self
        else:
            warnings.warn("Tried to add a report with a variable that is already registered. Skipping...")

    @classmethod
    def getitem(cls,key):
        """
        retrieves a certain report from the instances created.

        :param key: the ylabel of the respective report
        """
        return cls._instances[key]

    def add_data(self,x):
        """
        inserts some data into the data structure

        :param x: a scalar value
        """
        self.data.append(x)

    def plot_data(self,ax,s=1.8,color="black",scatter_color="gray"):
        """
        plots the data onto a matplotlib axis

        :param ax: a matplotlib axis
        """

        data = self.data
        x = np.arange(len(data)) + 1
        y = data # np.random.rand(len(x))

        if len(data) > 1 and data[1] is not None:
            has_labels = True

        ax.plot(x, y, "-", color=color) # <- manually optimized

        if len(y) < 20:
            ax.scatter(x, y, color=scatter_color, s=s)  # <- manually optimized

        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)

        # ax.set_title(self.title)


class DistributionReport:
    """
    A generic class for a logger of a distribution (i.e. )
    """

    def __init__(self,xlabel,ylabel,data=None):
        """
        :param xlabel: x axis title of the report
        :param ylabel: y axis title of the report
        :param data: initial data (default None). Has to have 'append' method, ideally a list of tuples (data_i, tag)
        """
        if data is not None:
            sorted_data = list(data.copy())
            sorted_data.sort(key = lambda x: x[0])
            self.data = sorted_data
        else:
            self.data = []

        self.xlabel = xlabel
        self.ylabel = ylabel

    def add_data(self, x, label=None):
        """
        adds data into the data structure. (stores a sorted version of x).

        :param x: list or numpy array to store
        :param label: some additional tag
        """

        y = np.sort(x.copy())

        # store distribution
        self.data.append((y,label))

    def plot_data(self, ax,color=None,s = None):
        """
        plot the data onto a matplotlib axis

        :param ax: a matplotlib axis
        :param color: plotting color
        :param s: scatter size
        """

        if color is None:
            col = "gray" # colors = ["gray", "indianred", "mediumblue"]
        else:
            col = color

        sorted_data = list(self.data.copy())
        sorted_data.sort(key = lambda x: x[0])

        if s is None:
            s = max(2.0, 8.0 - 4.0 * (len(sorted_data)/1000.0))

        for i,data in enumerate(sorted_data):
            x = data[0]
            y = data[1] # np.random.rand(len(x))

            # #ax.plot(x, y,color=colors[i%len(colors)], alpha=1-0.8*i/len(self.data[0]),label=label)
            ax.scatter(x, y, color=col, s= s)

        ax.set_ylabel(self.xlabel)
        ax.set_xlabel(self.ylabel)
        # ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


class ReportingSheet:
    """
    Reporting sheet is an overview sheet for reporting model results in form of a grid plot.
    """

    def __init__(self,instances=None):
        """
        :param instances: default None, if not None: list of Report instances can be passed here
        """
        if instances is None:
            self.items = []
        else:
            self.items = instances

    def add_report(self,report):
        """
        Adds a report item to this sheet.

        :param report: any IndicatorReport or DistributionReport
        """
        self.items.append(report)

    def plot(self, show_plot=True,verbose=False):
        """
        Generates a plot grid using matplotlib

        :param show_plot: show the figure in a window? default True. If False, figure is returned
        :param verbose: print number of rows and columns if True (default False)
        :return fig: matplotlib figure
        """

        import matplotlib.pyplot as plt
        plt.rcParams.update({'font.size': 8})

        # layout is 2 plots per column...
        
        if len(self.items) == 1:
            n_cols = 1
            n_rows = 1

        else:
            n_cols = 2
            n_rows = max(1,int(np.ceil(len(self.items)/n_cols)))

        if verbose: print("<Reporting Sheet> n_rows","n_cols",n_rows,n_cols)

        cm = 1 / 2.54  # centimeters in inches
        fig = plt.figure(figsize=(0.5*3.1415*10.5*cm,14.8*cm)) # DIN A6

        try:
            plt.style.use("macro")
        except:
            pass

        for i,item in enumerate(self.items):
            ax = fig.add_subplot(n_rows,n_cols,i+1)
            item.plot_data(ax)

        plt.tight_layout()
        fig.subplots_adjust(hspace=.47)

        if show_plot:
            plt.show()

        return fig

    def to_dataframe(self):
        """
        combines the data into a single pandas dataframe
        """
        df = pd.DataFrame()
        for i, item in enumerate(self.items):
            # TODO warn if something is overwritten

            if isinstance(item, IndicatorReport):
                df[item.xlabel] = list(range(len(item.data)))
                df[item.ylabel] = item.data

            elif isinstance(item, DistributionReport):
                df[item.xlabel] = [d[0] for d in item.data]
                df[item.ylabel] = [d[1] for d in item.data]

            else:
                warnigns.warn("Found strang item in Reporting sheet. Skipping. %s" % str(item))
        # df.index.name = self.items[0].xlabel
        return df

    def to_latex(self):
        """
        Generates latex code NOT YET IMPLEMENTED
        """
        raise NotImplementedError("Not yet implemented. Wait for beta release.")


if __name__ == "__main__":

    rep_sheet = ReportingSheet()

    for i in range(3):
        my_dist = DistributionReport(title="Distribution 1")
        my_dist.add_data(np.random.rand(10),label="t=1")
        my_dist.add_data(np.random.rand(10),label="t=2")
        my_dist.add_data(np.random.rand(10), label="t=3")
        rep_sheet.add_report(my_dist)

    for i in range(3):
        my_ind = IndicatorReport(xlabel="Time", ylabel="Some Indicator")
        my_ind.add_data(np.random.rand(10), label="t=1")
        my_ind.add_data(np.random.rand(10), label="t=2")
        my_ind.add_data(np.random.rand(10), label="t=3")
        rep_sheet.add_report(my_ind)

    rep_sheet.plot()
