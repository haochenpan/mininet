#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

start_redis = 'redis-server --daemonize yes --protected-mode no --port {0}'
load_ycsb = ('./bin/ycsb load redis -s -P workloads/workloada -p "redis.host=10.0.0.{0}" '
             '-p "redis.port={1}" -p recordcount={2} -p operationcount={3}')
run_ycsb = ('./bin/ycsb run redis -s -P workloads/workloada -p "redis.host=10.0.0.{0}" '
            '-p "redis.port={1}" -p recordcount={2} -p operationcount={3} > h{0}.txt')

# recordcount = 10000
# operationcount = 1000000

recordcount = 100
operationcount = 10000

def latency_gen():
    while True:
        for i in range(5):
            yield "%sms" % i

class MyTopo(Topo):
    def build(self):
        switches = []
        for i in range(5):
            switch = self.addSwitch('s%s' % (i + 1))
            host = self.addHost('h%s' % (i + 1))
            self.addLink(host, switch, bw=1000, delay=latency_gen())
            switches.append(switch)
        for i in range(len(switches) - 1):
            self.addLink(switches[i], switches[i + 1], bw=1000, delay=latency_gen())


def perfTest():
    def subTest(hostNum, hostPort):
        hn = net.get('h%s' % (hostNum))  # a redis host
        # hn.cmdPrint(start_redis.format(hostPort))
        # h1.cmdPrint("redis-cli -h 10.0.0.{0} -p {1} -n 0 ping".format(hostNum, hostPort))
        # h1.cmdPrint("cd ~/ycsb-0.15.0")
        h1.cmdPrint("ping 10.0.0.{0} -c 30 > h{0}.ping".format(hostNum))
        # h1.cmdPrint(load_ycsb.format(hostNum, hostPort, recordcount, operationcount))
        # h1.cmdPrint(run_ycsb.format(hostNum, hostPort, recordcount, operationcount))

    topo = MyTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll()
    h1 = net.get('h1')
    # h2 = net.get('h2')
    # h5 = net.get('h5')
    # net.iperf((h1, h2))
    # net.iperf((h1, h5))

    subTest(2, 6379)
    # subTest(3, 6380)
    # subTest(4, 6381)
    # subTest(5, 6382)

    # h1.cmdPrint("ps -fe | grep redis")
    # h1.cmdPrint("killall redis-server")
    # h1 rm h*.*

    # CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    perfTest()
    # l = latency_gen()
    # print l.next()
    # print l.next()
    # print l.next()
