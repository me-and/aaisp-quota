#!/usr/bin/python

# Convert log files to png graphs.  It's not pretty, but it works...
# Usage: xyakplot.py filein.csv fileout.png

import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import pandas

if __name__ == '__main__':
    data = pandas.read_csv(sys.argv[1], parse_dates=[0])

    plt.rcParams["figure.autolayout"] = True

    # Configure Y axis: input data is in bytes, but we want to display things
    # in GiB.
    plt.gca().set_ylabel("Quota (GiB)")
    plt.gca().set_ylim(bottom=0, top=1000000000000)
    plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(base=1024**3*100))
    plt.gca().set_yticklabels([int(y) // 1024**3 for y in plt.gca().get_yticks()])

    # Configure X axist: it's just datestamps.
    plt.gca().set_xlabel("Date")
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(base=7))
    plt.gca().xaxis.set_minor_locator(mticker.MultipleLocator(base=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))

    # Plot the data.
    plt.plot(data.Timestamp, data["Total quota"], color="xkcd:teal blue")
    plt.plot(data.Timestamp, data["Remaining quota"], color="xkcd:violet")

    # Save to the specified file.
    plt.savefig(sys.argv[2])
