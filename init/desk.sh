#!/usr/bin/env bash

requires() {
    if [ ! -f "$1" ]; then
        clear
        echo "required file *** $1 *** does not exists in the same dir"
        sleep 3
        return 1
    fi
}

copy_key() {
    mkdir -p ~/.ssh/
    cat id.pub >> ~/.ssh/authorized_keys
    rm id.pub
}

install_java() {
    sudo add-apt-repository ppa:openjdk-r/ppa -y
    sudo apt-get update
    sudo apt-get install openjdk-8-jdk -y
}

install_basic() {
    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install -y build-essential linux-headers-$(uname -r)
}

install_vnc() {
    sudo apt-get install -y vnc4server
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -yq ubuntu-desktop gnome-core
    sudo apt-get install -y gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal
    mkdir -p ~/.vnc/
    mv xstartup ~/.vnc/
    chmod 755 ~/.vnc/xstartup
}

install_dpkg() {
    sudo apt-get install -y make git zip ant
}

install_mininet() {
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
    sudo apt-get install yasm -y  # yasm for Kishori's library
    cd
    git clone https://github.com/kishori82/JavaISal.git
    git clone https://github.com/yingjianwu199868/cassandra.git
    cd cassandra
#    git checkout 0d464cd25ffbb5734f96c3082f9cc35011de3667
    git checkout treasErasure
    ant build
    cp -f ~/cassandra.yaml ~/cassandra/conf
    rm ~/cassandra.yaml
    cd
}


#key=id.pub
requires "$key" && copy_key

install_java
install_basic

key=xstartup
requires "$key" && install_vnc
install_dpkg
install_mininet
install_redis
install_ycsb

key=cassandra.yaml
requires "$key" && install_cass

# vncserver -geometry 1920x1080
# vncserver -geometry 3440x1440
# wireshark-gtk
# vncserver -kill :1


# https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=linux
# https://www.lifewire.com/how-to-install-the-pycharm-python-ide-in-linux-4091033
# export PATH="/root/pycharm-2019.1.3/bin:$PATH"