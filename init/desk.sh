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

install_redis() {
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

install_ycsb() {
    cd
    curl -O --location https://github.com/brianfrankcooper/YCSB/releases/download/0.15.0/ycsb-0.15.0.tar.gz
    tar xfvz ycsb-0.15.0.tar.gz
    rm -rf ycsb-0.15.0.tar.gz
}

install_cass() {
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

install_pycharm() {
# https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=linux
# https://www.lifewire.com/how-to-install-the-pycharm-python-ide-in-linux-4091033
    cd
    wget https://download-cf.jetbrains.com/python/pycharm-professional-2019.1.3.tar.gz
    tar xfz pycharm-professional-2019.1.3.tar.gz
    rm pycharm-professional-2019.1.3.tar.gz
}

install_bazel() {
# https://docs.bazel.build/versions/master/install-ubuntu.html
    cd
    wget https://github.com/bazelbuild/bazel/releases/download/0.26.0/bazel-0.26.0-installer-linux-x86_64.sh
    chmod +x bazel-0.26.0-installer-linux-x86_64.sh
    ./bazel-0.26.0-installer-linux-x86_64.sh --user
    rm bazel-0.26.0-installer-linux-x86_64.sh
    echo 'export PATH=$PATH:~/bin' >> ~/.bashrc
    source ~/.bashrc
}

install_onos() {
    cd
    git clone https://github.com/opennetworkinglab/onos.git
    cd onos
    git checkout onos-2.1
    bazel build onos
    cd

    # https://wiki.onosproject.org/display/ONOS/Downloads
    cd /opt
    ONOS_VERSION=2.1.0
    sudo wget http://repo1.maven.org/maven2/org/onosproject/onos-releases/2.1.0/onos-2.1.0.tar.gz
    sudo tar xzf onos-$ONOS_VERSION.tar.gz
    sudo mv onos-$ONOS_VERSION onos

}
# Java -> linux -> dpkg -> bazel -> onos -> vnc -> everything else

#key=id.pub
#requires "$key" && copy_key

#install_java
#install_basic

key=xstartup
requires "$key" && install_vnc
#install_dpkg

#install_bazel
#install_mininet
#install_redis

#install_ycsb

#key=cassandra.yaml
#requires "$key" && install_cass

# vncserver -geometry 1920x1080
# vncserver -geometry 3440x1440
# vncserver -geometry 1720x1440
# wireshark-gtk
# vncserver -kill :1



#git clone https://github.com/haochenpan/mininet-mgmt.git



#git clone https://gerrit.onosproject.org/onos


# https://wiki.onosproject.org/display/ONOS/Installing+on+a+single+machine
# https://wiki.onosproject.org/display/ONOS/Downloads

# https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
# https://askubuntu.com/questions/56104/how-can-i-install-sun-oracles-proprietary-java-jdk-6-7-8-or-jre
#wget https://download.oracle.com/otn/java/jdk/8u211-b12/478a62b7d4e34b78b671c754eaaf38ab/jdk-8u211-linux-x64.tar.gz?AuthParam=1559609241_f178508d4fdb6992052d4181625d5367
#mv jdk-8u211-linux-x64.tar.gz\?AuthParam\=1559609241_f178508d4fdb6992052d4181625d5367  jdk-8u211-linux-x64.tar.gz

#echo 'export PATH=$PATH:/usr/lib/jvm/jdk1.8.0_211/bin' >> ~/.bashrc

#echo 'export ONOS_ROOT=/home/panhi_bc_edu/onos' >> ~/.bashrc
#source ~/onos/tools/dev/bash_profile


#echo 'export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_211/' >> ~/.bashrc

# /opt/onos/bin/onos-service start
# http://35.237.65.237:8181/onos/ui/login.html