#!/usr/bin/python

"CS244 Assignment 2: Buffer Sizing"

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import lg
from mininet.util import dumpNodeConnections

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

# Time to run test
SECONDS_TO_RUN = 60

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
parser.add_argument('--delay',
                    dest="delay",
                    type=float,
                    help="Delay in milliseconds of host links",
                    default=1)
parser.add_argument('--dir', '-d',
                    dest="dir",
                    action="store",
                    help="Directory to store outputs",
                    default="results")
parser.add_argument('--nflows',
                    dest="nflows",
                    type=int,
                    action="store",
                    help="Number of subflows for MPTCP (1 indicates TCP)",
                    default=1)
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

# Experiment parameters
args = parser.parse_args()
CUSTOM_IPERF_PATH = args.iperf
DIR = os.path.join(args.dir, args.topo, args.workload)

if not os.path.exists(DIR):
    os.makedirs(DIR)

lg.setLogLevel('info')

def start_tcpprobe():
    "Install tcp_probe module and dump to file"
    os.system("rmmod tcp_probe 2>/dev/null; modprobe tcp_probe;")
    Popen("cat /proc/net/tcpprobe > %s/tcp_probe.txt" %
          args.dir, shell=True)

def stop_tcpprobe():
    os.system("killall -9 cat; rmmod tcp_probe &>/dev/null;")

def get_max_throughput(net):
    seconds = 10
    server, client = net.hosts[0], net.hosts[1]
    server.sendCmd("%s -s -p %s" %
                (CUSTOM_IPERF_PATH, 5001), shell=True)
    client.sendCmd("%s -c %s -p %s -t %d -yc" %
                   (CUSTOM_IPERF_PATH, server.IP(), 5001, seconds),
                   shell=True)
    throughput = client.waitOutput().split(',')[-1]
    os.system('killall -9 ' + CUSTOM_IPERF_PATH)
    return throughput

def get_topology():
    return FatTreeTopo()

def get_workload(net):
    return OneToOneWorkload(net, args.iperf, SECONDS_TO_RUN)

def print_to_file(max_throughput, output):
    filename = os.path.join(DIR, nflows)
    f = open(filename)
    f.write("%s\n%s\n" % (max_throughput, output.join(',')))
    f.close()

def main():
    "Create network and run Buffer Sizing experiment"

    start = time()
    topo = get_topology()
    net = Mininet(controller=RemoteController, topo=topo, host=CPULimitedHost,
                  link=TCLink, switch=OVSKernelSwitch)
    net.start()
    dumpNodeConnections(net.hosts)
    workload = get_workload(net)
    net.pingAll()

    max_throughput = get_max_throughput(net)

    enable_mptcp(args.mptcp_subflows)

    cprint("Starting experiment for workload %s with %i subflows" % (
               args.workload, args.nflows), "green")

    output = workload.run()
    if output:
        print_to_file(max_throughput, output)
    else:
        print "Initializing iperf connections failed"

    # Shut down iperf processes
    os.system('killall -9 ' + CUSTOM_IPERF_PATH)

    net.stop()
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

