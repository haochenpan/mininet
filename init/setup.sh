#!/usr/bin/env bash

function install_dependencies() {
    mkdir -p ~/.ssh/
    cat id.pub >> ~/.ssh/authorized_keys
    rm id.pub
    rm setup.sh

    sudo add-apt-repository ppa:openjdk-r/ppa -y
    sudo apt-get update
    sudo apt-get install openjdk-8-jdk -y
    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install build-essential linux-headers-$(uname -r) -y
    sudo apt-get install make git zip ant -y
}

function install_mininet() {
    cd
    mkdir mininet
    cd mininet
    git clone git://github.com/mininet/mininet.git
    cd mininet
    git checkout 2.2.2
    ./util/install.sh -a
    cd
}

function install_redis() {
    cd
    wget http://download.redis.io/redis-stable.tar.gz
    tar xvzf redis-stable.tar.gz
    cd redis-stable
    make
    sudo cp src/redis-server /usr/local/bin/
    sudo cp src/redis-cli /usr/local/bin/
    cd
    rm redis-stable.tar.gz
}

function install_ycsb() {
    cd
    curl -O --location https://github.com/brianfrankcooper/YCSB/releases/download/0.15.0/ycsb-0.15.0.tar.gz
    tar xfvz ycsb-0.15.0.tar.gz
    rm -rf ycsb-0.15.0.tar.gz
}

function install_cass() {
    cd
    git clone https://github.com/yingjianwu199868/cassandra.git
    cd cassandra
    git checkout treasOpt
    ant build
    cp -f ~/cassandra.yaml ~/cassandra/conf
    rm ~/cassandra.yaml
    cd
}


install_dependencies
install_mininet
install_redis
install_ycsb
install_cass

# mv ../home/panhi_bc_edu/id.pub ../home/panhi_bc_edu/setup.sh ../home/panhi_bc_edu/cassandra.yaml ./
# cp ./cassandra.yaml ~/cassandra/conf/
