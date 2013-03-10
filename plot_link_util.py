from util.helper import *
from collections import defaultdict
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-f', dest="files", nargs='+', required=True)
parser.add_argument('-o', '--out', dest="out", default=None)
parser.add_argument('-k', dest="k", default=None)

args = parser.parse_args()

def first(lst):
    return map(lambda e: e[0], lst)

def second(lst):
    return map(lambda e: e[1], lst)

"""
Sample line:
2.221032535 10.0.0.2:39815 10.0.0.1:5001 32 0x1a2a710c 0x1a2a387c 11 2147483647 14592 85
"""
def parse_file(f):
    times = defaultdict(list)
    cwnd = defaultdict(list)
    srtt = []
    for l in open(f).xreadlines():
        fields = l.strip().split(' ')
        if len(fields) != 10:
            break
        if fields[2].split(':')[1] != args.port:
            continue
        sport = int(fields[1].split(':')[1])
        times[sport].append(float(fields[0]))

        c = int(fields[6])
        cwnd[sport].append(c * 1480 / 1024.0)
        srtt.append(int(fields[-1]))
    return times, cwnd

added = defaultdict(int)
events = []

def constant_factory(value):
     return itertools.repeat(value).next

link_util = defaultdict(list)
for f in args.files:
  print f

  flow = f[f.find('flows') + len('flows')]
  output = []
  for line in open(f).xreadlines():
    link_util[flow].append(float(line))
  link_util[flow] = sorted(link_util[flow])

#TODO: TCP n=1 sorted order of data points
#tcp_points = [1,2,3,4,5]
#tcp_points = [float(x) / float(maxes['1']) for x in throughput['1']] 

#TODO: MPTCP n=8 sorted order of data points
#mptcp_points = [1,2,4,8,16]
#mptcp_points = [float(x) / float(maxes['8']) for x in throughput['8']] 

#TODO: read from file and average
#avgThroughput = (20, 35, 30, 35, 27, 5, 6, 7)

# set up plot
m.rc('figure', figsize=(16, 6))
fig = plt.figure()
title = 'Fat Tree (k=%s), One-to-one workload' % args.k
# plot rank of flow
axPlot = fig.add_subplot(1, 1, 1)
#axPlot.plot(first(cwnd_time), second(cwnd_time), lw=2, label="$MPTCP$")
#axPlot.plot(first(cwnd_time), second(cwnd_time), lw=2, label="$x$")
for flow in link_util:
    xaxis = range(len(link_util[flow]))
    if flow == '1':
        label = "TCP"
    else:
        label = "MPTCP, %s subflows" % flow
    axPlot.plot(xaxis, link_util[flow], lw=2, label=label)
#axPlot.grid(True)
axPlot.legend(loc='lower right')
axPlot.set_xlabel("Rank of Link")
axPlot.set_ylabel("Throughput (% of full link utilization)")
axPlot.set_title(title)

if args.out:
    print 'saving to', args.out
    plt.savefig(args.out)
else:
    plt.show()
