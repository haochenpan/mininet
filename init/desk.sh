#!/usr/bin/env bash

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
    sudo apt-get install build-essential linux-headers-$(uname -r) -y
}

install_vnc() {
    sudo apt-get install vnc4server -y
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -yq ubuntu-desktop gnome-core gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal
    mkdir -p ~/.vnc/
    mv xstartup ~/.vnc/
    chmod 755 ~/.vnc/xstartup
}

install_dpkg() {

    sudo apt-get install make git zip ant -y

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


install_java
install_basic
install_vnc
install_dpkg
install_mininet

# vncserver -geometry 1920x1080
# wireshark-gtk
# vncserver -kill :1