'''
Plot ping RTTs over time
'''
from util.helper import *
from collections import defaultdict
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--files', '-f',
                    help="Ping output files to plot",
                    required=True,
                    action="store",
                    nargs='+')

parser.add_argument('--freq',
                    help="Frequency of pings (per second)",
                    type=int,
                    default=10)

parser.add_argument('--out', '-o',
                    help="Output png file for the plot.",
                    default=None) # Will show the plot
parser.add_argument('-k', 
                    dest="k", 
                    help="Degree of the Fat Tree",
                    default=None)
parser.add_argument('-w', dest="workload", default=None)

args = parser.parse_args()

def parse_ping(fname):
    ret = []
    lines = open(fname).readlines()
    num = 0
    for line in lines:
        if 'bytes from' not in line:
            continue
        try:
            rtt = line.split(' ')[-2]
            rtt = rtt.split('=')[1]
            rtt = float(rtt)
            ret.append([num, rtt])
            num += 1
        except:
            break
    return ret

m.rc('figure', figsize=(8, 6))
fig = plt.figure()
axHist = fig.add_subplot(111)

pings = defaultdict(list)

for f in args.files:
  #print f
  if not f.find('ping'):
      continue

  flow = f[f.find('flows') + len('flows')]
  val = parse_ping(f)
  if len(val) == 0:
      continue
  avgVal = avg([x[1] for x in val])
  pings[flow].append(avgVal)

#print pings

avgPings = []
for flow in pings:
    avgPings.append(avg(pings[flow]))

N = 8
labels = ('TCP', '2', '3', '4', '5', '6', '7', '8')
xaxis = np.arange(N)  # the x locations for the groups
width = 0.5
xoffset = (1 - width) / 2
axHist.bar(xaxis + xoffset, avgPings, width, color='k') #, yerr=menStd)               
axHist.set_xlabel("No. of MPTCP Subflows")
axHist.set_ylabel("Average RTT (in ms)")
axHist.set_title("Fat Tree (k=%s), %s workload" % (args.k, args.workload))
axHist.set_xticks(xaxis + width/2 + xoffset)
axHist.set_xticklabels( labels )

if args.out:
    print 'saving to', args.out
    plt.savefig(args.out)
else:
    plt.show()
