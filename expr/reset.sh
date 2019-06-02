#!/usr/bin/env bash

curr=$(pwd)
cd ~/cassandra
echo "before reset"
git status

git reset --hard
cp ~/mgmt/expr/cassandra.yaml ~/cassandra/conf

echo "after reset"
git status
cd "$curr"