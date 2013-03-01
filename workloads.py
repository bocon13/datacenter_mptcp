#!/usr/bin/env python

from random import choice, shuffle
from subprocess import Popen, PIPE
from mininet.util import pmonitor
from time import sleep
import sys
import termcolor as T

def progress(t):
    while t > 0:
        print T.colored('  %3d seconds left       \r' % (t), 'cyan'),
        t -= 1
        sys.stdout.flush()
        sleep(1)
    print '\r\n'

class OneToOneWorkload():
    def __init__(self, net, iperf, seconds):
        self.iperf = iperf
        self.seconds = seconds
        self.mappings = []
        hosts = list(net.hosts)
        shuffle(hosts)
        group1, group2 = hosts[::2], hosts[1::2]
        self.create_mappings(list(group1), list(group2))
        self.create_mappings(group2, group1)

    def create_mappings(self, group1, group2):
        while group1:
            server = choice(group1)
            group1.remove(server)
            client = choice(group2)
            group2.remove(client)
            self.mappings.append((server, client))

    def run(self, dir):
        for mapping in self.mappings:
            server = mapping[0]
            server.popen("%s -s -p %s" %
                        (self.iperf, 5001), shell=True)
        for mapping in self.mappings:
            server, client = mapping
            client.popen("%s -c %s -p %s -t %d -yc -i 10 > %s/client_iperf-%s.txt" %
                          (self.iperf, server.IP(), 5001, self.seconds, dir,
                           client.name),
                           shell=True)

        progress(self.seconds + 15) # 15 second buffer to tear down connections and write output
