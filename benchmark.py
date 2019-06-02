import sys
from time import time
from sys import argv
from Queue import Queue
from threading import Thread
import string
import random
import ramcloud
import redis




# random.seed(a='755')


def random_chars(y): return ''.join(random.choice(string.ascii_letters) for _ in range(y))



class WorkloadGenerator(object):
    def __init__(self):

        # no need to change
        self.schema = 'cms.usertable'
        self.key_prefix = 'user'

        self.max_key_id = 10000000

        # parameter tuning
        self.record_count = 10000
        self.operation_count = 1000000
        self.read_proportion = 0.5  # update_proportion = 1 - self.read_proportion
        self.field_length_in_bytes = 100


        # private variables
        self.keys = set()
        self.keys_tuple = tuple()
        self.keys_vals = dict()

        self.read_op_acc = 0
        self.update_op_acc = 0
        self.read_time_acc = 0
        self.update_time_acc = 0


    def load(self):

        # 1. clear previous data
        self.keys = set()
        self.keys_tuple = tuple()
        self.keys_vals = dict()

        self.read_op_acc = 0
        self.update_op_acc = 0
        self.read_time_acc = 0
        self.update_time_acc = 0

        print "***************************************************"
        print "record_count,         ", self.record_count
        print "operation_count,      ", self.operation_count
        print "read_proportion,      ", self.read_proportion
        print "field_length_in_bytes,", self.field_length_in_bytes

        # 2. prepare keys & values
        while len(self.keys) < self.record_count:
            curr_val = random.randint(0, self.max_key_id)
            curr_key = self.key_prefix + str(curr_val)
            if curr_key not in self.keys:
                self.keys.add(curr_key)
        self.keys_tuple = tuple(self.keys)

        for k in self.keys:
            v = random_chars(self.field_length_in_bytes)
            self.keys_vals[k] = v

        # 3. load to database
        def load_ramcloud():
            c = ramcloud.RAMCloud()
            c.connect('basic+udp:host=127.0.0.1,port=11000', 'main')
            c.drop_table(self.schema)
            c.create_table(self.schema)
            t = c.get_table_id(self.schema)


            try:
                for k, v in self.keys_vals.items():
                    c.write(t, k, v)
            except Exception as e:
                print repr(e)

        def load_redis():
            r = redis.Redis(host='10.0.0.1', port=6379, db=0)
            r.flushall()

            try:
                for k, v in self.keys_vals.items():
                    r.set(k, v)
            except Exception as e:
                print repr(e)

        # load_ramcloud()
        load_redis()


    def run(self):

        # 4. run (read and update)
        def get_operation_type():
            v = random.random()
            return 'read' if v <= self.read_proportion else 'update'

        def run_ramcloud():
            c = ramcloud.RAMCloud()
            c.connect('basic+udp:host=127.0.0.1,port=11000', 'main')
            c.create_table(self.schema)
            t = c.get_table_id(self.schema)

            try:
                for i in range(self.operation_count):
                    operation_type = get_operation_type()

                    if operation_type == 'read':
                        k = random.choice(self.keys_tuple)

                        t1 = time()
                        v = c.read(t, k)[0]
                        self.read_time_acc += (time() - t1)
                        self.read_op_acc += 1

                        if self.keys_vals[k] != v:
                            raise Exception
                    else:
                        k = random.choice(self.keys_tuple)
                        v = random_chars(self.field_length_in_bytes)

                        t1 = time()
                        c.write(t, k, v)
                        self.update_time_acc += (time() - t1)
                        self.update_op_acc += 1

                        self.keys_vals[k] = v

                    # print operation_type, k, v

            except Exception as e:
                print repr(e)

        def run_redis():
            r = redis.Redis(host='10.0.0.1', port=6379, db=0)
            try:
                for i in range(self.operation_count):
                    operation_type = get_operation_type()

                    if operation_type == 'read':
                        k = random.choice(self.keys_tuple)

                        t1 = time()
                        v = r.get(k)
                        self.read_time_acc += (time() - t1)
                        self.read_op_acc += 1

                        if self.keys_vals[k] != v:
                            raise Exception
                    else:
                        k = random.choice(self.keys_tuple)
                        v = random_chars(self.field_length_in_bytes)

                        t1 = time()
                        r.set(k, v)
                        self.update_time_acc += (time() - t1)
                        self.update_op_acc += 1

                        self.keys_vals[k] = v

                    # print operation_type, k, v
            except Exception as e:
                print repr(e)

        start = time()
        # run_ramcloud()
        run_redis()
        run_time = time() - start
        print "[OVERALL], RunTime(s),", run_time
        print "[OVERALL], Throughput(ops/sec),", self.operation_count / run_time
        print "[READ], Operations,", self.read_op_acc
        print "[READ], AverageLatency(us),", self.read_time_acc * (10 ** 6) / self.read_op_acc
        print "[UPDATE], Operations,", self.update_op_acc
        print "[UPDATE], AverageLatency(us), ", self.update_time_acc * (10 ** 6) / self.update_op_acc



if __name__ == '__main__':
    wg = WorkloadGenerator()
    for i in range(5):
        wg.load()
        wg.run()
