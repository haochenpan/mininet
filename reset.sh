#!/usr/bin/env bash

cd ~/cassandra
echo "before reset"
git status

git reset --hard
cp ~/mgmt/init/cassandra.yaml ~/cassandra/conf

echo "after reset"
git status