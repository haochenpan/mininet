#!/usr/bin/env bash

function install_cass() {
    cd
#    git clone https://github.com/yingjianwu199868/cassandra.git
    git clone https://github.com/ZezhiWang/cassandra.git
    cd cassandra
    git checkout 0d464cd25ffbb5734f96c3082f9cc35011de3667
    ant build
    cp -f ~/mgmt/cassandra.yaml ~/cassandra/conf
    cd
}

install_cass

# cp ./cassandra.yaml ~/cassandra/conf/