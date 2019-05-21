#!/usr/bin/python

from os import system
from sys import argv
from time import sleep

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

short_sleep = 2
long_sleep = 10

master_ip = "10.0.0.1"
master_port = 6379

start_redis = 'redis-server --daemonize yes --protected-mode no --save "" --port {0}'
start_redis_slave = 'redis-server --daemonize yes --protected-mode no --save "" --port {0} --slaveof {1} {2}'


class RedisTopo(Topo):
    """
        build a Mininet topology with one switch,
        and each host is connected to the switch.
    """

    def build(self, n=3):
        switch = self.addSwitch('s%s' % 1)
        for i in range(n):
            host = self.addHost('h%s' % (i + 1))
            self.addLink(host, switch)


def clean():
    system("killall redis-server")  # kill Cassandra threads
    system("mn --clean")  # perform Mininet clean
    print "wait the system to stabilize..."
    sleep(short_sleep)


def startMini():
    """
    Start Mininet with mounted directories
    :return:
    """
    setLogLevel('info')
    topo = RedisTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.addNAT().configDefault()
    net.start()
    net.pingAll()
    hs = [net.get('h{0}'.format(i + 1)) for i in range(3)]
    dumpNodeConnections(net.hosts)
    # net.stop()
    return net, hs


def startRedis(hs):
    print "starting 3 Redis instances, may take a while..."
    hs[0].cmd(start_redis.format(6379))
    hs[1].cmd(start_redis_slave.format(6380, master_ip, master_port))
    hs[2].cmd(start_redis_slave.format(6381, master_ip, master_port))


def cleanUp():
    print "interupt"
    system("killall redis-server")  # kill Cassandra threads
    system("mn --clean")  # perform Mininet clean


def main():
    clean()
    if '-t' in argv or '--topo' in argv:
        net, hs = startMini()
        if '-s' in argv or '--start' in argv:
            startRedis(hs)
        CLI(net)


if __name__ == '__main__':
    if len(argv) == 1 or ('-h' in argv or '--help' in argv):
        print """
        usage:
        switches: 
            -h or --help  : show this help
            -s or --start : start 3 Redis nodes
            -t or --topo  : build a Mininet topology of 3 hosts and 1 switch
              """
    else:
        print "switches are: ", argv[1:]
        main()
