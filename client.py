#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
About: Simple client.
"""

import time
import os

SERVICE_PORT = 5566
IP_SERVERS = ['10.0.0.1', '10.0.0.2']
INTERVAL = 5


def mycmd(SERVICE_IP):
    os.system('iperf -c {} -p {}'.format(SERVICE_IP, SERVICE_PORT))


if __name__ == "__main__":
    file = open('./log/serverIP.log', 'r')
    
    while True:
        Lines = file.readlines()
        for line in Lines:
            # quando si rileva un calo della larghezza di banda scriviamo 'change'
            if('change' in line):
                for ip in IP_SERVERS:
                    mycmd(ip)
                    time.sleep(3) # diamo tempo all'iperf di terminare
                time.sleep(INTERVAL) # leggere ogni INTERVAL secondi
            else:
                current_ip = line.split('\n')[0]
                mycmd(current_ip)
                time.sleep(3)
