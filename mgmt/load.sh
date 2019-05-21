#!/usr/bin/env bash

cd ~/cassandra
./bin/cqlsh 10.0.0.1 -e "create keyspace ycsb WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor': 5};"
./bin/cqlsh 10.0.0.1 -e "create table ycsb.usertable (y_id varchar primary key, field0 varchar);"
