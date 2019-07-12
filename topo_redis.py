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

ycsb_file_path = "~/data_redis.txt"
num_of_hosts = 5

recordcount = 20000
operationcount = 2000000
# recordcount = 100
# operationcount = 10000

master_ip = "10.0.0.2"
port = 6379  # for all Redis instances

start_redis = 'redis-server --daemonize yes --protected-mode no --save "" --port {0}'
start_redis_slave = 'redis-server --daemonize yes --protected-mode no --save "" --port {0} --slaveof {1} {2}'

load_ycsb = ('~/ycsb-0.15.0/bin/ycsb load redis -s -P ~/mgmt/ycsb/workloads/workload_5 -p "redis.host={0}" '
             '-p "redis.port={1}" -p recordcount={2} -p operationcount={3}')
runs_ycsb = ('~/ycsb-0.15.0/bin/ycsb run  redis -s -P ~/mgmt/ycsb/workloads/workload_5 -p "redis.host={0}" '
             '-p "redis.port={1}" -p recordcount={2} -p operationcount={3} >> {4}')


class RedisTopo(Topo):
    """
        build a Mininet topology with one switch,
        and each host is connected to the switch.
    """

    def build(self):
        switch = self.addSwitch('s%s' % 1)
        for i in range(num_of_hosts):
            host = self.addHost('h%s' % (i + 1))
            self.addLink(host, switch)


def startMini():
    setLogLevel('info')
    topo = RedisTopo()
    net = Mininet(topo=topo)
    # net = Mininet(topo=topo, link=TCLink)
    net.addNAT().configDefault()
    net.start()
    net.pingAll()
    hs = [net.get('h{0}'.format(i + 1)) for i in range(num_of_hosts)]
    dumpNodeConnections(net.hosts)
    return net, hs


def startRedis(hs):
    print "starting 3 Redis instances, may take a while..."
    hs[1].cmd(start_redis.format(port))
    # hs[2].cmd(start_redis_slave.format(port, master_ip, port))
    # hs[3].cmd(start_redis_slave.format(port, master_ip, port))


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

    if '-s' in argv or '--start' in argv:
        startRedis(hs)

    if '-e' in argv or '--eval' in argv:
        hs[0].cmd("cd ~/ycsb-0.15.0")
        hs[0].cmdPrint(load_ycsb.format(master_ip, port, recordcount, operationcount))
        hs[0].cmdPrint(runs_ycsb.format(master_ip, port, recordcount, operationcount, ycsb_file_path))
    else:
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
