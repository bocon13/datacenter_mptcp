#!/usr/bin/env python

from random import choice

class OneToOneWorkload():
    def __init__(self, net, iperf, seconds):
        self.iperf = iperf
        self.seconds = seconds
        self.mappings = []
        hosts = list(net.hosts)
        while hosts:
            server = choice(hosts)
            hosts.remove(server)
            client = choice(hosts)
            hosts.remove(client)
            self.mappings.append((server, client))

    def run(self):
        for mapping in self.mappings:
            server, client = mapping
            server.sendCmd("%s -s -p %s" %
                        (self.iperf, 5001))
            client.sendCmd("%s -c %s -p %s -t %d -yc" %
                          (self.iperf, server.IP(), 5001, self.seconds))

        results = []
        for mapping in self.mappings:
            results.append(mapping[1].waitOutput().split(',')[-2:])
            # results is list of (bytes transferred, bandwidth)
        return results
