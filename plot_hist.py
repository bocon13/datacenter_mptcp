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

throughput = defaultdict(list)
max_throughput = 0 
for f in args.files:
  #print f

  flow = f[f.find('flows') + len('flows')]
  output = []
  for line in open(f).xreadlines():
    output.append(line)
  if len(output) > 0:
    val = output[-2].rstrip().split(',')[-1]
    #print flow, val

    if f.find('client') >= 0:
      throughput[flow].append(float(val))
    else:
      max_throughput = float(val)
  else:
    #print "         ERROR!!!!!!!!!!!!!!!!!!!"  
    pass

#print throughput 

avgThroughput = []
tcp_points = []
mptcp_points = []
for i in sorted(throughput.keys()):
  #print i 
  vals = [ 100 * x / max_throughput  for x in throughput[i] ] 
  avgThroughput.append(avg(vals))
  if i == '1':
    tcp_points = sorted(vals)
  if i == '8':
    mptcp_points = sorted(vals)

#print avgThroughput
#print max_throughput

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
axPlot = fig.add_subplot(1, 2, 2)
#axPlot.plot(first(cwnd_time), second(cwnd_time), lw=2, label="$MPTCP$")
#axPlot.plot(first(cwnd_time), second(cwnd_time), lw=2, label="$x$")
xaxis = range(len(mptcp_points))
axPlot.plot(xaxis, mptcp_points, lw=2, label="MPTCP, 8 subflows")
xaxis = range(len(tcp_points))
axPlot.plot(xaxis, tcp_points, lw=2, label="TCP")
#axPlot.grid(True)
axPlot.legend(loc='lower right')
axPlot.set_xlabel("Rank of Flow")
axPlot.set_ylabel("Throughput (% of optimal)")
axPlot.set_title( title )

# plot histogram
N = 8
labels = ('TCP', '2', '3', '4', '5', '6', '7', '8')
xaxis = np.arange(N)  # the x locations for the groups
width = 0.5 
xoffset = (1 - width) / 2
axHist = fig.add_subplot(1, 2, 1)
axHist.bar(xaxis + xoffset, avgThroughput, width, color='k') #, yerr=menStd)
axHist.set_xlabel("No. of MPTCP Subflows")
axHist.set_ylabel("Throughput (% of optimal)")
axHist.set_title( title )
axHist.set_xticks(xaxis + width/2 + xoffset)
axHist.set_xticklabels( labels )

if args.out:
    print 'saving to', args.out
    plt.savefig(args.out)
else:
    plt.show()
