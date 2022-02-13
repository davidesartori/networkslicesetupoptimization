#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
About: Simple server.
"""

import iperf3

SERVICE_PORT = 5566
INTERVAL = 5
LOG_FILE = './log/iperf_log.log'

def init():
    server = iperf3.Server()
    server.bind_address = '10.0.0.1'
    server.port = 5566
    server.protocol = 'udp'
    server.verbose = False
    return server


if __name__ == "__main__":
    file = open(LOG_FILE, "a")
    server = init()
    while True:
        result = server.run()
        if result.error:
            file.write(result.error)
        else:
            file.write('  Client ip: {}'.format(result.remote_host))
            file.write('  Kilobits per second  (kbps)  {0}'.format(result.kbps))

