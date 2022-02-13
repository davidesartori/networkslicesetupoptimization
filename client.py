#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
About: Simple client.
"""

import time

# Ip degli host selezionati come server
IP_SERVERS = ['10.0.0.1', '10.0.0.2']
INTERVAL = 5


client = iperf3.Client()
client.port = 5566
client.protocol = 'udp'


def iperf(ip):
    client.server_hostname = '{}'.format(ip)
    result = client.run()


if __name__ == "__main__":
    file = open('./log/server_ip_log.log', 'r')
    
    while True:
        Lines = file.readlines()
        for line in Lines:
            if('change' in line):
                for ip in IP_SERVERS:
                    iperf(ip)
                    time.sleep(3) # diamo tempo all'iperf di terminare
            else:
                current_ip = line.split('\n')[0]
                iperf(current_ip)
                time.sleep(3)

            time.sleep(INTERVAL) # leggere ogni INTERVAL secondi
