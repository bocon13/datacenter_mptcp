#!/usr/bin/env python

from random import choice

CUSTOM_IPERF_PATH = 'iperf'
seconds = 10

class OneToOneWorkload():
    def __init__(self, net):
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
                        (CUSTOM_IPERF_PATH, 5001))
            client.sendCmd("%s -c %s -p %s -t %d -yc" %
                          (CUSTOM_IPERF_PATH, server.IP(), 5001, seconds))

        results = []
        for mapping in self.mappings:
            results.append(mapping[1].waitOutput().split(',')[-2:])
            # results is list of (bytes transferred, bandwidth)
        return results
