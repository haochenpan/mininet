#!/usr/bin/env bash

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

copy_key() {
    mkdir -p ~/.ssh/
    echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDDanWUjBsv+jyKE1YRPVzhv10UoffG5GWFf/fHdrYkpg87s3pQ5Lz+Zi+mX6WPRuTCieThnzpi6ARtOuVewAPEYak/+Ln7c7Lxs7hU0SiuzWefwRj7LjC7siy4HhXydCO1klr57Uc4HyFNWJI+6aC7BhLfvRiQ3qOkLgRhDznkLEQCpFzNAt+SOAQhs50shY0zqO3v8RgPeqyBrSGPItpHtiL+m0ky/sNQrQi/9oN8SuzA3HGHUvdcMSVyBqzPha0T5ZUGx1mvl0G+v2jBi6IFDglqiQOpi5OaLZOZPN6sHD3lrFXfaI4Nn+TmKmFJVNVgihYubFXChFwjzeBxbHPT root' >> ~/.ssh/authorized_keys
}

install_basics() {
    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install -y build-essential linux-headers-$(uname -r)
    sudo apt-get install -y make git zip pkg-config libzmq3-dev
}

install_go() {
    cd /usr/local
    sudo wget https://dl.google.com/go/go1.12.6.linux-amd64.tar.gz
    sudo tar -C /usr/local -xzf go1.12.6.linux-amd64.tar.gz
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
    source ~/.bashrc
    go get github.com/pebbe/zmq4
    go get -u github.com/go-redis/redis
#    go get github.com/peterbourgon/diskv
    cd
}

#copy_key
install_basics
#install_mininet
install_go
install_redis
