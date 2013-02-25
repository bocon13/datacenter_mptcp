#!/usr/bin/env python

from random import choice

class OneToOneWorkload():
    def __init__(self, net):
        self.mappings = []
        hosts = list(net.hosts)
        while hosts:
            server, client = choice(hosts), choice(hosts)
            self.mappings.append((server, client))
            hosts.remove(server)
            hosts.remove(client)
    def run(net):
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
