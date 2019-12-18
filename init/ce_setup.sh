#!/usr/bin/env bash
function install_dependencies() {
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

function install_cass() {
  cd
  git clone https://github.com/ZezhiWang/cassandra.git
  cd cassandra
  git checkout 0d464cd25ffbb5734f96c3082f9cc35011de3667
  ant build
}

install_dependencies
install_mininet
install_cass

# cassandra.yaml what I changed:
# seed_provider.seeds
# listen_address -> listen_interface: eth0
# rpc_address -> rpc_interface: eth0
# auto_snapshot: false