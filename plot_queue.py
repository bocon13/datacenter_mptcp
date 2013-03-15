'''
Plot queue occupancy over time
'''
from util.helper import *
# import plot_defaults

from matplotlib.ticker import MaxNLocator
from pylab import figure


parser = argparse.ArgumentParser()
parser.add_argument('--files', '-f',
                    help="Queue timeseries output to one plot",
                    required=True,
                    action="store",
                    nargs='+',
                    dest="files")

parser.add_argument('--legend', '-l',
                    help="Legend to use if there are multiple plots.  File names used as default.",
                    action="store",
                    nargs="+",
                    default=None,
                    dest="legend")

parser.add_argument('--out', '-o',
                    help="Output png file for the plot.",
                    default=None, # Will show the plot
                    dest="out")

parser.add_argument('--labels',
                    help="Labels for x-axis if summarising; defaults to file names",
                    required=False,
                    default=[],
                    nargs="+",
                    dest="labels")

parser.add_argument('--every',
                    help="If the plot has a lot of data points, plot one of every EVERY (x,y) point (default 1).",
                    default=1,
                    type=int)
parser.add_argument('-k', dest="k", default=None)
parser.add_argument('-w', dest="workload", default=None)

args = parser.parse_args()

if args.legend is None:
    args.legend = []
    for file in args.files:
        args.legend.append(file)

to_plot=[]

colors = []
def get_colors(num_intf=10):
    for r in range(num_intf):
        for g in range(num_intf):
            for b in range(num_intf):
                colors.append('#%02x%02x%02x'
                             % (r*255/num_intf, g*255/num_intf, b*255/num_intf))

from random import randint
def get_style(i):
    return colors[randint(0, len(colors) - 1)]

m.rc('figure', figsize=(8, 6))
fig = figure()
title = 'Fat Tree (k=%s), %s workload' % (args.k, args.workload)
ax = fig.add_subplot(111)
get_colors()
for i, f in enumerate(args.files):
    data = read_list(f)
    xaxis = map(float, col(0, data))
    start_time = xaxis[0]
    xaxis = map(lambda x: x - start_time, xaxis)
    qlens = map(float, col(1, data))

    xaxis = xaxis[::args.every]
    qlens = qlens[::args.every]
    ax.plot(xaxis, qlens, lw=2, color=get_style(i))
    ax.xaxis.set_major_locator(MaxNLocator(4))

plt.ylabel("Packets")
plt.xlabel("Seconds")

if args.out:
    print 'saving to', args.out
    plt.savefig(args.out)
else:
    plt.show()
