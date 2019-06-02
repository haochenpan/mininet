#!/usr/bin/python

import atexit
from os import system
from sys import argv

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

short_sleep = 2
long_sleep = 10

num_of_hosts = 5

start_redis = 'redis-server --daemonize yes --protected-mode no --save ""'

class RedisTopo(Topo):
    """
        build a Mininet topology with one switch,
        and each host is connected to the switch.
    """

    def build(self):
        switch = self.addSwitch('s%s' % 1)
        for i in range(num_of_hosts):
            host = self.addHost('h%s' % (i + 1))
            self.addLink(host, switch, delay='5ms')


def startMini():
    setLogLevel('info')
    topo = RedisTopo()
    # net = Mininet(topo=topo)
    net = Mininet(topo=topo, link=TCLink)
    net.addNAT().configDefault()
    net.start()
    net.pingAll()
    hs = [net.get('h{0}'.format(i + 1)) for i in range(num_of_hosts)]
    dumpNodeConnections(net.hosts)
    return net, hs



def cleanUp():
    system("killall redis-server")  # kill redis threads
    system("mn --clean")  # perform Mininet clean


def main():
    # cleanUp()
    if '-t' in argv or '--topo' in argv:
        net, hs = startMini()
        atexit.register(cleanUp)
    else:
        return

    CLI(net)


if __name__ == '__main__':
    if len(argv) == 1 or ('-h' in argv or '--help' in argv):
        print """
        usage:
            python topo_redis.py -t -s -e
        switches: 
            -h or --help  : show this help
            -s or --start : start 3 Redis nodes
            -t or --topo  : build a Mininet topology of 3 hosts and 1 switch
            -e or --evla  : start YCSB benchmarking
              """
    else:
        system("clear")
        print "switches are: ", argv[1:]
        main()
