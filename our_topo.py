#!/usr/bin/env python

from mininet.topo import Topo

class FatTreeTopo(Topo):
    def __init__(self, k=4, bw=1):
        super(FatTreeTopo, self).__init__()
        self.k = k
        self.bw = bw
	self.create_topo()

    def create_topo(self):
	k = self.k
        hosts = [ 'h%i' % x for x in range(k*k)]
        core_switches = [ 'cs%i' % x for x in range(k)]
        agg_switches = [ 'as%i' % x for x in range(2*k)]
        edge_switches = [ 'es%i' % x for x in range(2*k)]
        all_switches = core_switches + agg_switches + edge_switches
        nodes = {}
        for h in hosts:
            nodes[h] = self.addHost(h)
        for sw in all_switches:
            nodes[sw] = self.addSwitch(sw)
        # Set up layer 0 <-> layer 1
        for i in range(k):
            x = 0 if i < k/2 else 1
            while x < 2*k:
                self.addLink(nodes[core_switches[i]],
                             nodes[agg_switches[x]])
                x += 2
        # Set up layer 1 <-> layer 2
        for i in range(2*k):
            self.addLink(nodes[agg_switches[i]],
                         nodes[edge_switches[i]])
            if i % 2 == 0:
                self.addLink(nodes[agg_switches[i]],
                             nodes[edge_switches[i+1]])
            else:
                self.addLink(nodes[agg_switches[i]],
                             nodes[edge_switches[i-1]])
        # Set up layer 2 <-> layer 3
        for i in range(2*k):
            self.addLink(nodes[edge_switches[i]],
                         nodes[hosts[2*i]])
            self.addLink(nodes[edge_switches[i]],
                         nodes[hosts[2*i + 1]])

