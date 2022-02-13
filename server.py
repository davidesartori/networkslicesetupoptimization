#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
About: Simple server.
"""

import os

SERVICE_PORT = 5566
INTERVAL = 5
LOG_FILE = './log/iperf.log'


def mycmd():
    os.system('iperf -s -p {} >> {}'.format(SERVICE_PORT, LOG_FILE))


if __name__ == "__main__":
    
    while True:
        mycmd()
