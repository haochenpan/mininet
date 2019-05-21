#!/usr/bin/env bash

# ssh-keygen -m PEM -f id -C root
# cat /home/panhi_bc_edu/id.pub >> ~/.ssh/authorized_keys

# ssh -i id -o StrictHostKeyChecking=no systopicsgroup3_gmail_com@34.73.189.158
mkdir -p ~/.ssh/
cat id.pub >> ~/.ssh/authorized_keys
rm id.pub
rm setup.sh

#echo "alias mme='cd ~/mininet/mininet/examples/'" >> ~/.bashrc
#echo "alias sp='sudo python'" >> ~/.bashrc

sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install build-essential linux-headers-$(uname -r) -y
sudo apt-get install make git zip ant -y
sudo apt-get install python-pip -y


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
    sudo add-apt-repository ppa:openjdk-r/ppa -y
    sudo apt-get update
    sudo apt-get install openjdk-8-jdk -y
    cd
    curl -O --location https://github.com/brianfrankcooper/YCSB/releases/download/0.15.0/ycsb-0.15.0.tar.gz
    tar xfvz ycsb-0.15.0.tar.gz
    rm -rf ycsb-0.15.0.tar.gz
}

#install_mininet
#install_redis
install_ycsb


# mv ../home/panhi_bc_edu/id.pub ../home/panhi_bc_edu/setup.sh ./


# mn --link tc,bw=10,delay=1ms  # ping says lat is 4 ms
# h1 redis-server --daemonize yes --protected-mode no
# h1 redis-cli -n 0 ping
# h2 redis-cli -h 10.0.0.1 -n 0 ping

# h2 cd ycsb-0.15.0
# h2 ./bin/ycsb load redis -s -P workloads/workloada -p "redis.host=10.0.0.1 " -p "redis.port=6379" -p recordcount=1000000 -p operationcount=1000000
# h2 ./bin/ycsb run  redis -s -P workloads/workloada -p "redis.host=10.0.0.1 " -p "redis.port=6379" -p recordcount=1000000 -p operationcount=1000000 >> outputLoad.txt


#  mn --clean && killall redis-server && ps -fe | grep redis