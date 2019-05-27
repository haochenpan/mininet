#!/usr/bin/env bash

cd ~/cassandra
./bin/cqlsh 10.0.0.1 -e "create keyspace ycsb WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor': 5};"
./bin/cqlsh 10.0.0.1 -e "CREATE TABLE ycsb.usertable(y_id varchar PRIMARY KEY, field0 varchar, field1 varchar, tag1 varchar, field2 varchar, tag2 varchar, field3 varchar, tag3 varchar);"
