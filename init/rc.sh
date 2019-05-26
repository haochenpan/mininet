#!/usr/bin/env bash

# https://zookeeper.apache.org/doc/r3.3.3/zookeeperStarted.html#sc_Download
# http://apache.claz.org/zookeeper/stable/
# https://ramcloud.atlassian.net/wiki/spaces/RAM/pages/6848614/General+Information+for+Developers


sudo add-apt-repository ppa:openjdk-r/ppa -y
sudo apt-get update
sudo apt-get install openjdk-8-jdk -y
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install build-essential linux-headers-$(uname -r) -y
sudo apt-get install make git zip ant -y

# for ramcloud
sudo apt-get install aptitude -y
aptitude install git-core doxygen libboost-all-dev libpcre3-dev protobuf-compiler -y
aptitude install libprotobuf-dev libcrypto++-dev libevent-dev libzookeeper-mt-dev -y

# zookeeper (for ramcloud)
wget http://apache.claz.org/zookeeper/stable/apache-zookeeper-3.5.5-bin.tar.gz
tar -xzf apache-zookeeper-3.5.5-bin.tar.gz

git clone https://github.com/PlatformLab/RAMCloud.git
cd RAMCloud
git submodule update --init --recursive
ln -s ../../hooks/pre-commit .git/hooks/pre-commit

make -j12


obj.master/server -L tcp:host=`hostname -s`,port=1101 -x zk:rcmaster:2181 --totalMasterMemory 16000 -f /dev/sda2 --segmentFrames 10000 -r 2