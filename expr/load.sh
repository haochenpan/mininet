#!/usr/bin/env bash

cd ~/cassandra
./bin/cqlsh 10.0.0.1 -e "create keyspace ycsb WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor': 3};"
./bin/cqlsh 10.0.0.1 -e "CREATE TABLE ycsb.usertable(y_id varchar PRIMARY KEY, field0 varchar);"
