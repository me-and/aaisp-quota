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
    data.Timestamp = data.Timestamp.map(lambda t: t.tz_convert('Europe/London'))

    plt.rcParams["figure.autolayout"] = True

    # Configure Y axis: input data is in bytes, but we want to display things
    # in GiB.
    plt.gca().set_ylabel("Quota (GiB)")
    plt.gca().set_ylim(bottom=0, top=2000000000000)
    plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(base=1024**3*200))
    plt.gca().set_yticklabels([int(y) // 1024**3 for y in plt.gca().get_yticks()])

    # Configure X axist: it's just datestamps.
    plt.gca().set_xlabel("Date")
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(base=7))
    plt.gca().xaxis.set_minor_locator(mticker.MultipleLocator(base=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))

    # Plot the data.
    plt.plot(data.Timestamp, data["Total quota"])
    plt.plot(data.Timestamp, data["Remaining quota"])

    start_timestamp = data.Timestamp[0].replace(hour=0, minute=0, second=0)
    if start_timestamp.month == 12:
        end_timestamp = start_timestamp.replace(year=start_timestamp.year + 1, month=1)
    else:
        end_timestamp = start_timestamp.replace(month=start_timestamp.month + 1)
    plt.plot((start_timestamp, end_timestamp), (data["Remaining quota"][0], 0))
    plt.plot((start_timestamp, end_timestamp), (data["Total quota"][0], 0))

    # Save to the specified file.
    plt.savefig(sys.argv[2])
