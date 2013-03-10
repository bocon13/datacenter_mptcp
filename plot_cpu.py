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


added = defaultdict(int)
events = []

def constant_factory(value):
     return itertools.repeat(value).next

utilization = defaultdict(dict)
for f in args.files:
  #print f

  topo = int(re.findall('ft([0-9]+)/', f)[0])
  flow = int(re.findall('flows([0-9]+)/', f)[0])
  output = []
  for line in open(f).xreadlines():
    output.append(line)
  if len(output) > 0:
    val = output[-1].rstrip().split(' ')[-1]
    #print topo, flow, val
    utilization[topo][flow] = 100.0 - float(val)
  else:
    #print "         ERROR!!!!!!!!!!!!!!!!!!!"  
    pass

#print utilization

x_labels = []
y_plot = defaultdict(list)
for topo in sorted(utilization.keys()):
  if len(utilization[topo].keys()) == 8:
    x_labels.append("k = %d" % topo)
    for f in sorted(utilization[topo].keys()):
      y_plot[f].append(utilization[topo][f])

# set up plot
m.rc('figure', figsize=(8, 6))
fig = plt.figure()
title = 'CPU Utilization, One-to-one workload'
# plot rank of flow

xaxis = np.arange(len(x_labels))  # the x locations for the groups
width = 0.1
xoffset = (1 - width*len(y_plot.keys())) / 2
axHist = fig.add_subplot(1, 1, 1)

colors = ['#ff0000','#ff7f00','#ffff00','#00ff00','#00ffff', '#0000ff', '#4B0082', '#8F00FF']
for flows in sorted(y_plot.keys()):
  axHist.bar(xaxis + xoffset + (flows-1) * width, y_plot[flows], width, 
              color= colors[flows-1], #'k' if flows % 2 == 0 else 'b', 
              label='TCP' if flows == 1 else 'MPTCP, %d flows' % flows ) #, yerr=menStd)

axHist.set_xlabel("Size of Fat Tree Topology")
axHist.set_ylabel("% CPU Utilization")

axHist.set_title( title )
axHist.set_xticks(xaxis + width*len(y_plot.keys())/2 + xoffset)
axHist.set_xticklabels( x_labels )

axHist.legend(loc='upper left')

if args.out:
    print 'saving to', args.out
    plt.savefig(args.out)
else:
    plt.show()
