import gevent
from gevent import monkey
monkey.patch_all()

from websocket import create_connection

import random
import time

spawn_count = 10000


def random_hash():
    return "%032x" % random.getrandbits(128)

count = 0
error = 0


start_time = time.time()


def echo():
    global count
    global error

    try:
        ws = create_connection('ws://localhost:8000/echo')
    except:
        time.sleep(1)
        ws = create_connection('ws://localhost:8000/echo')
    start_time = time.time()
    cur_time = time.time()
    while cur_time - start_time < 10.0:
        value = random_hash()
        ws.send(value)
        result = ws.recv()
        count += 1
        if result != value:
            error += 1
        cur_time = time.time()
        time.sleep(1)
    ws.close()

gevent.joinall(
    [gevent.spawn(echo) for i in xrange(0, spawn_count)]
)

print "echo: %i, error: %i, echo per sec: %f" % (
    count, error, count/(time.time()-start_time))
