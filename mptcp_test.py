#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import Host
from mininet.link import TCLink
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import lg
from mininet.util import dumpNodeConnections, custom

import subprocess
from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
import termcolor as T
from argparse import ArgumentParser

import sys
import os
#from util.monitor import monitor_qlen
#from util.helper import stdev

from mptcp_util import enable_mptcp, reset
from dctopo import FatTreeTopo
from workloads import OneToOneWorkload

def cprint(s, color, cr=True):
    """Print in color
       s: string to print
       color: color to use"""
    if cr:
        print T.colored(s, color)
    else:
        print T.colored(s, color),


# Parse arguments
parser = ArgumentParser(description="Host throughput tests")
parser.add_argument('--bw', '-b',
                    dest="bw",
                    type=float,
                    action="store",
                    help="Bandwidth of links",
                    default=10)
parser.add_argument('--queue', '-q',
                    dest="q",
                    type=int,
                    action="store",
                    help="Queue size (in packets)",
                    default=10)
parser.add_argument('--dir', '-d',
                    dest="dir",
                    action="store",
                    help="Directory to store outputs",
                    default="results")
parser.add_argument('--workload',
                    dest="workload",
                    action="store",
                    help="Type of workload",
                    required=True)
parser.add_argument('--topology',
                    dest="topo",
                    action="store",
                    help="Datacenter topology",
                    required=True)
parser.add_argument('--iperf',
                    dest="iperf",
                    action="store",
                    help="Custom path for iperf",
                    required=True)
parser.add_argument('--time', '-t',
                    dest="time",
                    type=int,
                    action="store",
                    help="Length of experiment in seconds",
                    default=60)

# Experiment parameters
args = parser.parse_args()
CUSTOM_IPERF_PATH = args.iperf

lg.setLogLevel('info')

def start_tcpprobe():
    "Install tcp_probe module and dump to file"
    os.system("rmmod tcp_probe 2>/dev/null; modprobe tcp_probe;")
    Popen("cat /proc/net/tcpprobe > %s/tcp_probe.txt" %
          args.dir, shell=True)

def stop_tcpprobe():
    os.system("killall -9 cat; rmmod tcp_probe &>/dev/null;")

def get_max_throughput(net, output_dir):
    reset()
    print "Finding max throughput..."
    seconds = 20
    server, client = net.hosts[0], net.hosts[1]
    server.popen("%s -s -p %s" %
                (CUSTOM_IPERF_PATH, 5001), shell=True)
    proc = client.popen("%s -c %s -p %s -t %d -yc -i 10 > %s/max_throughput.txt" %
                   (CUSTOM_IPERF_PATH, server.IP(), 5001, seconds, output_dir), shell=True)
    
    proc.communicate()
    os.system('killall -9 ' + CUSTOM_IPERF_PATH)

def get_topology(output_dir):
    if args.topo.find('ft') == 0:
      K = int(args.topo[2:])
      print 'fat tree with %d' % K 

      pox_c = Popen("exec ~/pox/pox.py --no-cli riplpox.riplpox --topo=ft,%s --routing=hashed --mode=reactive 1> %s/pox.out 2> %s/pox.out" % (K, output_dir, output_dir), shell=True)
      sleep(1) # wait for controller to start
      return FatTreeTopo(k=K), pox_c

def get_workload(net):
    if args.workload == "one_to_one":
        return OneToOneWorkload(net, args.iperf, args.time)
    else if args.workload == "one_to_several":
        return OneToSeveralWorkload(net, args.iperf, args.time)
    else:
        return AllToAllWorkload(net, args.iperf, args.time)

def main():
    top_dir = os.path.join(args.dir, args.topo, args.workload)
    if not os.path.exists(top_dir):
        os.makedirs(top_dir)

    start = time()
    topo, pox_c = get_topology(top_dir)
    link = custom(TCLink, bw=args.bw, max_queue_size=args.q) #, delay=args.delay)
    net = Mininet(controller=RemoteController, topo=topo, host=Host,
                  link=link, switch=OVSKernelSwitch)
    net.start()

    workload = get_workload(net)
    #net.pingAll()
    sleep(3)
    #CLI(net)

    get_max_throughput(net, top_dir)

    for nflows in range(1, 9):
        cwd = os.path.join(top_dir, "flows%d" % nflows)

        if not os.path.exists(cwd):
            os.makedirs(cwd)
        enable_mptcp(nflows)

        cprint("Starting experiment for workload %s with %i subflows" % (
                args.workload, nflows), "green")

        workload.run(cwd)

        # Shut down iperf processes
        os.system('killall -9 ' + CUSTOM_IPERF_PATH)

    net.stop()

    # kill pox controller
    pox_c.kill()
    pox_c.wait()

    Popen("killall -9 top bwm-ng tcpdump cat mnexec", shell=True).wait()
    end = time()
    reset()
    cprint("Experiment took %.3f seconds" % (end - start), "yellow")

if __name__ == '__main__':
    try:
        main()
    except:
        print "-"*80
        print "Caught exception.  Cleaning up..."
        print "-"*80
        import traceback
        reset()
        traceback.print_exc()
        os.system("killall -9 top bwm-ng tcpdump cat mnexec iperf; mn -c")

