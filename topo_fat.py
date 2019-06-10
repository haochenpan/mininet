#!/usr/bin/python

from functools import partial
from os import system
from sys import argv
from time import sleep
import atexit
from threading import Thread

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI


def indexGen(prefix):
    i = 1
    while True:
        yield '%s%s' % (prefix, i)
        i += 1


class FatTree(Topo):

    def __init__(self):
        self.coreSwitchList = []
        self.aggSwitchList = []
        self.edgeSwitchList = []
        self.hostList = []
        self.sgen = indexGen("s")
        self.hgen = indexGen("h")

        Topo.__init__(self)

    def build(self, *args, **params):
        c, a, e = 3, 3, 5
        # c, a, e = 1, 1, 2
        for i in range(c):
            self.coreSwitchList.append(self.addSwitch(next(self.sgen)))

        for i in range(a):
            self.aggSwitchList.append(self.addSwitch(next(self.sgen)))

        for i in range(e):
            self.edgeSwitchList.append(self.addSwitch(next(self.sgen)))

        for core in self.coreSwitchList:
            for agg in self.aggSwitchList:
                self.addLink(core, agg)

        for agg in self.aggSwitchList:
            for edge in self.edgeSwitchList:
                self.addLink(agg, edge)

        for edge in self.edgeSwitchList:
            for i in range(2):
                host = self.addHost(next(self.hgen))
                self.hostList.append(host)
                self.addLink(edge, host)

topos = { 'fattree' : ( lambda : FatTree()) }

# if __name__ == '__main__':
#     pass
#     setLogLevel('info')
#     topo = FatTree()
#     net = Mininet(topo=topo)
#     net.start()
