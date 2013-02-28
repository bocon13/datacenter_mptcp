#!/usr/bin/env python

from random import choice, shuffle

class OneToOneWorkload():
    def __init__(self, net, iperf, dir, seconds):
        self.iperf = iperf
        self.dir = dir
        self.seconds = seconds
        self.mappings = []
        hosts = list(net.hosts)
        shuffle(hosts)
        group1, group2 = hosts[::2], hosts[1::2]
        self.create_mappings(list(group1), list(group2))
        self.create_mappings(group2, group1)

    def create_mappings(self, group1, group2)
        while group1:
            server = choice(group1)
            group1.remove(server)
            client = choice(group2)
            group2.remove(client)
            self.mappings.append((server, client))

    def count_connections():
        "Count current connections in iperf output file"
        out = self.dir + "/iperf_server.txt"
        lines = Popen("grep connected %s | wc -l" % out,
                      shell=True, stdout=PIPE).communicate()[0]
        return int(lines)

    def verify_connections(self):
        succeeded = 0
        wait_time = 300
        while wait_time > 0 and succeeded != nflows:
            wait_time -= 1
            succeeded = count_connections()
            print 'Connections %d/%d succeeded\r' % (succeeded, nflows),
            sys.stdout.flush()
            sleep(1)
        if succeeded != nflows:
            print 'Giving up'
            return False
        return True

    def run(self):
        for mapping in self.mappings:
            server, client = mapping
            server.sendCmd("%s -s -p %s > %s/iperf_server.txt" %
                        (self.iperf, 5001, self.dir))
            client.sendCmd("%s -c %s -p %s -t %d -yc" %
                          (self.iperf, server.IP(), 5001, self.seconds))

        if not self.verify_connections():
            return None

        results = []
        for mapping in self.mappings:
            results.append(mapping[1].waitOutput().split(',')[-1])
            # results is list of host throughputs
        return results
