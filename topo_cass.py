#!/usr/bin/python

from functools import partial
from os import system
from sys import argv
from time import sleep

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

short_sleep = 7
long_sleep = 17


class CassTopo(Topo):
    """
        build a Mininet topology with one switch,
        and each host is connected to the switch.
    """

    def build(self):
        switch = self.addSwitch('s%s' % 1)
        for i in range(5):
            host = self.addHost('h%s' % (i + 1))
            self.addLink(host, switch)


def clean():
    system("killall java")  # kill Cassandra threads
    system("mn --clean")  # perform Mininet clean
    if '-c' in argv or '--clean' in argv:
        system("rm ~/cassandra/data -rf")
        system("rm ~/cassandra/logs -rf")
    if '-f' in argv or '--force' in argv:
        system("ant clean -f ~/cassandra/build.xml")
    if '-b' in argv or '--build' in argv:
        system("ant build -f ~/cassandra/build.xml")
    else:
        print "wait the system to stabilize..."
        sleep(short_sleep)


def startMini():
    """
    Start Mininet with mounted directories
    :return:
    """
    setLogLevel('info')
    topo = CassTopo()
    privateDirs = [('~/cassandra/logs', '~/cassandra/logs/%(name)s'),
                   ('~/cassandra/data', '~/cassandra/data/%(name)s')]
    host = partial(Host, privateDirs=privateDirs)
    net = Mininet(topo=topo, host=host, link=TCLink)
    net.addNAT().configDefault()
    net.start()
    net.pingAll()

    # change network interface cards' names to suit cassandra.yaml
    hs = [net.get('h{0}'.format(i + 1)) for i in range(5)]
    for i in range(5):
        hs[i].intf('h{0}-eth0'.format(i + 1)).rename('eth0')

    dumpNodeConnections(net.hosts)
    # net.stop()
    return net, hs


def startCass(hs):
    """
    Start Cassandra program at each host
    :param hs: a list of hosts
    :return:
    """
    print "starting 5 cass instances, may take a while..."
    for i in range(5):
        # if not redirect output, cass may stuck at bootstrap
        hs[i].cmd("~/cassandra/bin/cassandra -R &>/dev/null")
        sleep(short_sleep)
        print "cass node %s is alive" % (i + 1)
    print "wait the system to stabilize..."
    sleep(long_sleep)
    o1 = hs[0].cmdPrint("~/cassandra/bin/nodetool status")

    # if want to drop table:
    if '-d' in argv or '--drop' in argv:
        hs[0].cmdPrint('~/cassandra/bin/cqlsh 10.0.0.1 -e "drop keyspace ycsb"')

    # if want to load table:
    if '-l' in argv or '--load' in argv:
        print "num of nodes joined: ", o1.count("UN")
        if o1.count("UN") == 5:
            hs[0].cmd(". ~/mgmt/load.sh")
            hs[0].cmdPrint('~/cassandra/bin/cqlsh 10.0.0.1 -e "describe ycsb.usertable"')
            hs[0].cmdPrint("~/cassandra/bin/nodetool status")

        else:
            print "Not enough servers joined, please try manually"


def main():
    clean()
    if '-t' in argv or '--topo' in argv:
        net, hs = startMini()
        if '-s' in argv or '--start' in argv:
            startCass(hs)
        CLI(net)


if __name__ == '__main__':
    if len(argv) == 1 or ('-h' in argv or '--help' in argv):
        print """
        usage: python topo_cass.py -h                or --help
               python topo_cass.py -c                or --clean
               python topo_cass.py -t -s             or --topo --start
               python topo_cass.py -c -t -s -l       or --clean --topo --start --load (recommended)
               python topo_cass.py -t -s -d -l       or --topo --start --drop --load
               python topo_cass.py -c -b -t -s -l    or --clean --build --topo --start --load
               python topo_cass.py -c -f -b -t -s -l or --clean --force --build --topo --start --load (recommended)
        switches: 
            -b or --build : perform ant build
            -c or --clean : perform os clean, i.e. rm ~/cassandra/data and rm ~/cassandra/logs
            -d or --drop  : try to drop ycsb keyspace
            -f or --force : perform ant clean
            -h or --help  : show this help
            -l or --load  : try to load ycsb.usertable (use ~/cassandra/load.sh)
            -s or --start : start 5 cassandra nodes
            -t or --topo  : build a Mininet topology of 5 hosts and 1 switch
              """
    else:
        print "switches are: ", argv[1:]
        main()
