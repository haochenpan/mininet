#!/usr/bin/env bash

# http://apache.claz.org/zookeeper/stable/

# to install
# https://ramcloud.atlassian.net/wiki/spaces/RAM/pages/6848614/General+Information+for+Developers

# to run
# https://ramcloud.atlassian.net/wiki/spaces/RAM/pages/6848532/Setting+Up+a+RAMCloud+Cluster
# https://ramcloud.atlassian.net/wiki/spaces/RAM/pages/6848545/Service+Locators

mkdir -p ~/.ssh/
cat id.pub >> ~/.ssh/authorized_keys
rm id.pub

# common packages
clear
sudo add-apt-repository ppa:openjdk-r/ppa -y
sudo apt-get update
sudo apt-get install openjdk-8-jdk -y
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install build-essential linux-headers-$(uname -r) -y
sudo apt-get install make git zip ant python-pip -y

# for ramcloud
sudo apt-get install aptitude -y
aptitude install git-core doxygen libboost-all-dev libpcre3-dev protobuf-compiler libgtest-dev -y
aptitude install libprotobuf-dev libcrypto++-dev libevent-dev libzookeeper-mt-dev libssl-dev -y
sudo update-ca-certificates -f


# zookeeper (for ramcloud)
wget http://apache.claz.org/zookeeper/stable/apache-zookeeper-3.5.5-bin.tar.gz
tar -xzf apache-zookeeper-3.5.5-bin.tar.gz
rm apache-zookeeper-3.5.5-bin.tar.gz
mv ~/zoo.cfg ~/apache-zookeeper-3.5.5-bin/conf/

git clone https://github.com/PlatformLab/RAMCloud.git
cd RAMCloud
git submodule update --init --recursive
ln -s ../../hooks/pre-commit .git/hooks/pre-commit
make -j12
make install
cd

echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/RAMCloud/obj.master/' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/JavaISal/javaexample/' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/RAMCloud/install/lib/ramcloud/' >> ~/.bashrc
echo 'export PYTHONPATH=PYTHONPATH:~/RAMCloud/bindings/python/' >> ~/.bashrc
source ~/.bashrc

~/apache-zookeeper-3.5.5-bin/bin/zkServer.sh start

# https://zookeeper.apache.org/doc/r3.3.3/zookeeperStarted.html#sc_Download
#

# obj.master/coordinator -C basic+udp:host=127.0.0.1,port=11000  -x zk:127.0.0.1:2181 &
# obj.master/coordinator -C basic+udp:host=10.0.0.1,port=11000  -x zk:10.0.0.1:2181 &
# obj.master/server -L basic+udp:host=127.0.0.1,port=11001 -x zk:127.0.0.1:2181 --totalMasterMemory 1600 -f /dev/sda1 --segmentFrames 100 -r 0 &

# client
# https://ramcloud.atlassian.net/wiki/spaces/RAM/pages/6848598/Python+Bindings
# https://github.com/PlatformLab/RAMCloud/issues/30

# ~/apache-zookeeper-3.5.5-bin/bin/zkServer.sh stop


# g++ -std=c++11 -Iinstall/include -o Test src/TestClient.cc  -Linstall/lib/ramcloud -lramcloud -Lsrc -Isrc -Lobj.master -Iobj.master
#./Test basic+udp:host=127.0.0.1,port=11000

#scp -i ./init/id root@35.237.65.237:/root/RAMCloud/src/TestClient.cc ./

#c.connect(serverLocator='basic+udp:host=127.0.0.1,port=11000',clusterName='main')


bin/zkCli.sh 10.0.0.1:2181