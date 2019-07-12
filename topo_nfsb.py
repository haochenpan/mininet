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

from time import sleep

port = 6379
num_of_hosts = 7
start_redis = 'redis-server --daemonize yes --protected-mode no --save "" --port {0}'

cd_gnf = "cd ~/go/src/NFSB"
cd_controller = "cd ~/go/src/NFSB/Controller"
run_gnf = "go run gnfmain.go gnf -ip=10.0.0.1 &"
run_controller = "go run *.go benchmark 5"
check_run = "ls"

class RedisTopoSingleSwitch(Topo):
    """
        build a Mininet topology with one switch,
        and each host is connected to the switch.
    """

    def build(self):
        switch = self.addSwitch('s%s' % 1)
        for i in range(num_of_hosts):
            host = self.addHost('h%s' % (i + 1))
            # self.addLink(host, switch)
            self.addLink(host, switch, delay='1ms')


class RedisTopoLinear(Topo):

    def build(self):
        switches = []

        for i in range(num_of_hosts):
            switch = self.addSwitch('s%s' % (i + 1))
            switches.append(switch)
            host = self.addHost('h%s' % (i + 1))
            # self.addLink(host, switch)
            self.addLink(host, switch, delay='1ms')

        for i, e in enumerate(switches):
            if i == len(switches) - 1:
                break
            # self.addLink(switches[i + 1], switches[i])
            self.addLink(switches[i + 1], switches[i], delay='1ms')


def startMini():
    setLogLevel('info')
    if '-s' in argv or '--single' in argv:
        topo = RedisTopoSingleSwitch()
    elif '-l1' in argv or '--linear1' in argv or '-l2' in argv or '--linear2' in argv:
        topo = RedisTopoLinear()
    else:
        return
    # net = Mininet(topo=topo)
    net = Mininet(topo=topo, link=TCLink)
    net.addNAT().configDefault()
    net.start()
    net.pingAll()
    hs = [net.get('h{0}'.format(i + 1)) for i in range(num_of_hosts)]
    dumpNodeConnections(net.hosts)
    return net, hs


def startGGGRRR(hs):
    hs[1].cmd(cd_gnf)
    hs[1].cmd(run_gnf)
    hs[2].cmd(cd_gnf)
    hs[2].cmd(run_gnf)
    hs[3].cmd(cd_gnf)
    hs[3].cmd(run_gnf)
    hs[4].cmd(start_redis.format(port))
    # hs[5].cmd(start_redis.format(port))
    # hs[6].cmd(start_redis.format(port))
    sleep(5)
    hs[0].cmdPrint(cd_controller)
    hs[0].cmdPrint(run_controller)


def startGRGRGR(hs):
    hs[1].cmd(cd_gnf)
    hs[1].cmd(run_gnf)
    hs[2].cmd(start_redis.format(port))

    hs[3].cmd(cd_gnf)
    hs[3].cmd(run_gnf)
    hs[4].cmd(start_redis.format(port))

    hs[5].cmd(cd_gnf)
    hs[5].cmd(run_gnf)
    hs[6].cmd(start_redis.format(port))
    sleep(5)
    hs[0].cmdPrint(cd_controller)
    hs[0].cmdPrint(run_controller)


def cleanUp():
    system("killall redis-server")  # kill redis threads
    system("mn --clean")  # perform Mininet clean


def main():
    # cleanUp()
    net, hs = startMini()
    atexit.register(cleanUp)

    if '-r' in argv or '--redis' in argv:
        if '-s' in argv or '--single' in argv:
            startGGGRRR(hs)
        elif '-l1' in argv or '--linear1' in argv:
            startGRGRGR(hs)
        elif '-l2' in argv or '--linear2' in argv:
            startGGGRRR(hs)
    CLI(net)


if __name__ == '__main__':
    if len(argv) == 1 or ('-h' in argv or '--help' in argv):
        print """
        usage:
            python topo_redis.py -t -s
        switches: 
            -h or --help  : show this help
            -r or --redis : start 3 Redis nodes
            -s or --single  : 
            -l or --linear  : 
              """
    else:
        system("clear")
        print "flags are: ", argv[1:]
        main()
