#!/usr/bin/python

from os import system
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

start_redis = 'redis-server --daemonize yes --protected-mode no --port {0}'
start_redis_slave = 'redis-server --daemonize yes --protected-mode no --port {0} --slaveof {1} {2}'

load_ycsb = ('./bin/ycsb load redis -s -P workloads/workloada -p "redis.host=10.0.0.{0}" '
             '-p "redis.port={1}" -p recordcount={2} -p operationcount={3}')
run_ycsb = ('./bin/ycsb run redis -s -P workloads/workloada -p "redis.host=10.0.0.{0}" '
            '-p "redis.port={1}" -p recordcount={2} -p operationcount={3} > h{0}.txt')

# recordcount = 10000
# operationcount = 1000000

recordcount = 100
operationcount = 10000


class MyTopo(Topo):
    def build(self):
        switches = []
        for i in range(5):
            switch = self.addSwitch('s%s' % (i + 1))
            host = self.addHost('h%s' % (i + 1))
            self.addLink(host, switch)
            switches.append(switch)
        for i in range(len(switches) - 1):
            self.addLink(switches[i], switches[i + 1])


def perfTest():
    def subTest(hostNum, hostPort):
        hn = net.get('h%s' % (hostNum))  # a redis host
        # hn.cmdPrint(start_redis.format(hostPort))
        # h1.cmdPrint("redis-cli -h 10.0.0.{0} -p {1} -n 0 ping".format(hostNum, hostPort))
        # h1.cmdPrint("cd ~/ycsb-0.15.0")
        # h1.cmdPrint("ping 10.0.0.{0} -c 30 > h{0}.ping".format(hostNum))
        # h1.cmdPrint(load_ycsb.format(hostNum, hostPort, recordcount, operationcount))
        # h1.cmdPrint(run_ycsb.format(hostNum, hostPort, recordcount, operationcount))

    topo = MyTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll()
    hs = [net.get('h{0}'.format(i + 1)) for i in range(5)]
    hs[1].cmdPrint(start_redis.format(6379))
    hs[2].cmdPrint(start_redis_slave.format(6380, "10.0.0.2", 6379))
    hs[3].cmdPrint(start_redis_slave.format(6381, "10.0.0.2", 6379))

    # net.iperf((h1, h2))
    # net.iperf((h1, h5))

    # subTest(2, 6379)
    # subTest(3, 6380)
    # subTest(4, 6381)
    # subTest(5, 6382)

    hs[0].cmdPrint("ps -fe | grep redis")
    # hs[0].cmdPrint("redis-cli -h 10.0.0.{0} -p {1} -n 0 ping".format(2, 6379))
    # hs[0].cmdPrint("redis-cli -h 10.0.0.{0} -p {1} -n 0 ping".format(3, 6380))
    # hs[0].cmdPrint("redis-cli -h 10.0.0.{0} -p {1} -n 0 ping".format(4, 6381))
    hs[0].cmdPrint("redis-cli -h 10.0.0.{0} -p {1} -n 0 INFO replication > ~/info".format(2, 6379))
    hs[0].cmdPrint("redis-cli -h 10.0.0.{0} -p {1} -n 0 INFO replication >> ~/info".format(3, 6380))
    hs[0].cmdPrint("redis-cli -h 10.0.0.{0} -p {1} -n 0 INFO replication >> ~/info".format(4, 6381))
    # h1.cmdPrint("killall redis-server")
    # h1 rm h*.*

    CLI(net)
    # net.stop()


if __name__ == '__main__':
    system("mn --clean")
    system("killall redis-server")
    system("ps -fe | grep redis")
    setLogLevel('info')
    perfTest()
