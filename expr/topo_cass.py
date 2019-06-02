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

short_sleep = 5
long_sleep = 20
num_of_cass = 2
num_of_ycsb = 3


class CassTopo(Topo):
    """
        build a Mininet topology with one switch,
        and each host is connected to the switch.
    """

    def build(self):
        switch = self.addSwitch('s%s' % 1)
        for i in range(num_of_cass + num_of_ycsb):
            host = self.addHost('h%s' % (i + 1))
            self.addLink(host, switch)


def startMini():
    """
    Start Mininet with mounted directories
    :return:
    """
    setLogLevel('info')
    topo = CassTopo()
    privateDirs = [('~/cassandra/logs', '~/cassandra/logs/%(name)s'),
                   ('~/cassandra/data', '~/cassandra/data/%(name)s'),
                   ('~/mgmt/data', '~/mgmt/data/%(name)s')]
    host = partial(Host, privateDirs=privateDirs)
    net = Mininet(topo=topo, host=host)
    # net = Mininet(topo=topo, host=host, link=TCLink)
    net.addNAT().configDefault()
    net.start()
    net.pingAll()

    hs = [net.get('h{0}'.format(i + 1)) for i in range(num_of_cass + num_of_ycsb)]

    # change network interface cards' names to suit cassandra.yaml
    for i in range(num_of_cass):
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
    print "starting cass instances, may take a while..."
    for i in range(num_of_cass):
        # if not redirect output, cass may stuck at bootstrap
        hs[i].cmd("~/cassandra/bin/cassandra -R &>/dev/null")
        sleep(short_sleep)
        print "cass node %s is alive" % (i + 1)
    print "wait the system to stabilize..."
    sleep(long_sleep)
    o1 = hs[0].cmdPrint("~/cassandra/bin/nodetool status")

    # if want to drop table:
    if '-d' in argv or '--drop' in argv:
        hs[0].cmdPrint('~/cassandra/bin/cqlsh 10.0.0.1 -e "DROP KEYSPACE ycsb"')

    # if want to load table:
    if '-l' in argv or '--load' in argv:
        print "num of nodes joined: ", o1.count("UN")
        if o1.count("UN") == num_of_cass:
            hs[0].cmd(". ~/mgmt/load.sh")
            hs[0].cmdPrint('~/cassandra/bin/cqlsh 10.0.0.1 -e "describe ycsb.usertable"')
            hs[0].cmdPrint("~/cassandra/bin/nodetool status")

        else:
            print "Not enough servers joined, please try manually"


def evalCass(hs):
    def loadKeyspace():
        hs[5].cmd(". ~/mgmt/load.sh")

    def dropKeyspace():
        hs[5].cmdPrint('~/cassandra/bin/cqlsh 10.0.0.1 -e "DROP KEYSPACE ycsb"')

    def describeTable():
        hs[5].cmdPrint('~/cassandra/bin/cqlsh 10.0.0.1 -e "DESCRIBE ycsb.usertable"')

    def truncateTable():
        hs[5].cmdPrint('~/cassandra/bin/cqlsh 10.0.0.1 -e "TRUNCATE ycsb.usertable;"')

    def countTable():
        hs[5].cmdPrint('~/cassandra/bin/cqlsh 10.0.0.1 -e "SELECT COUNT(*) FROM ycsb.usertable;"')

    def run_at_one_client(host_index, client_idx, thread_cnt, read_ptn, field_len, ycsb_pse):
        hs[host_index].cmdPrint('~/mgmt/trial.sh {0} {1} {2} {3} {4}'
                                .format(client_idx, thread_cnt, read_ptn, field_len, ycsb_pse))

    def run_at_all_clients(thread_cnt, read_ptn, field_len, ycsb_pse):
        t1 = Thread(target=run_at_one_client, args=(5, 0, thread_cnt, read_ptn, field_len, ycsb_pse))
        t2 = Thread(target=run_at_one_client, args=(6, 1, thread_cnt, read_ptn, field_len, ycsb_pse))
        t3 = Thread(target=run_at_one_client, args=(7, 2, thread_cnt, read_ptn, field_len, ycsb_pse))
        for t in [t1, t2, t3]:
            t.start()
        for t in [t1, t2, t3]:
            t.join()

    def run_wl(thread_cnt, read_ptn, field_len):
        truncateTable()
        countTable()
        run_at_all_clients(thread_cnt, read_ptn, field_len, "load")
        countTable()
        run_at_all_clients(thread_cnt, read_ptn, field_len, "run")

    def run_wl_5_times(thread_cnt, read_ptn, field_len):
        run_wl(thread_cnt, read_ptn, field_len)
        run_wl(thread_cnt, read_ptn, field_len)
        run_wl(thread_cnt, read_ptn, field_len)
        run_wl(thread_cnt, read_ptn, field_len)
        run_wl(thread_cnt, read_ptn, field_len)

    def run_wl_vary_read(thread_cnt, field_len):
        for i in [1, 3, 5, 7, 9]:
            run_wl_5_times(thread_cnt, i, field_len)

    def run_wl_vary_size(thread_cnt, read_ptn):
        for i in [1, 4, 16, 64, 256, 1024]:  # 32 not in
            run_wl_5_times(thread_cnt, read_ptn, i)

    def run_wl_vary_thread(read_ptn, field_len):
        for i in [2, 4, 6, 8, 12]:  # 10 not in
            run_wl_5_times(i, read_ptn, field_len)

    dropKeyspace()
    loadKeyspace()
    describeTable()
    # run_wl_5_times(8, 5, 100)
    run_wl_vary_thread(9, 32)  # 10 not in, see below
    run_wl_vary_size(10, 9)  # 32 not in, see below
    run_wl_vary_read(10, 32)


def clean():
    cleanUp()
    if '-c' in argv or '--clean' in argv:
        system("rm ~/cassandra/data -rf")
        system("rm ~/cassandra/logs -rf")
        system("rm ~/mgmt/data -rf")
    if '-f' in argv or '--force' in argv:
        system("ant clean -f ~/cassandra/build.xml")
    if '-b' in argv or '--build' in argv:
        system("ant build -f ~/cassandra/build.xml")
    else:
        print "wait the system to stabilize..."
        sleep(short_sleep)


def cleanUp():
    system("killall java")  # kill Cassandra threads
    system("mn --clean")  # perform Mininet clean


def main():
    clean()
    if '-t' in argv or '--topo' in argv:
        net, hs = startMini()
        atexit.register(cleanUp)
    else:
        return

    if '-s' in argv or '--start' in argv:
        startCass(hs)
        if '-e' in argv or '--eval' in argv:
            evalCass(hs)

    CLI(net)


if __name__ == '__main__':
    if len(argv) == 1 or ('-h' in argv or '--help' in argv):
        print """
        usage: python topo_cass.py -h                or --help
               python topo_cass.py -c                or --clean
               python topo_cass.py -t -s             or --topo --start
               python topo_cass.py -c -t -s -e       or --clean --topo --start --eval (recommended)
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
        system("clear")
        print "switches are: ", argv[1:]
        main()

# ~/cassandra/bin/nodetool --host 10.0.0.1
# ~/cassandra/bin/cqlsh 10.0.0.1
# ssh -i ~/mgmt/init/id simulator-2 ~/mininet/mininet/util/m h3 ifconfig
