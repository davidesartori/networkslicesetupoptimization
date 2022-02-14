"""
Author: Gruppo 22 Networking II
Description: Implementation of network monitoring
"""

from re import I
import time

THRESHOLD = 200 #Kbits/s
CURRENT_BDW = 0


def monitoring():
    file_in = open('./log/iperf_log.log', 'r')
    file_out = open('./log/server.log', 'a')
    Lines = file_in.readlines()
    #{ip_server: [bandwidth, client_counter]}
    servers = {}
    for line in Lines:
        if('#' in line):
            if(len(servers)==1):
                server = list(servers)[0]
                current_bdw = calculate_avg_bandwidth(servers[server][0], servers[server][1])
                print(current_bdw)
                if((current_bdw-CURRENT_BDW+THRESHOLD) < 0):
                    file_out.write('migrate\n')
                    time.sleep(3)
            else:
                best_server = find_best_server(servers)
                CURRENT_BDW = best_server[1]
                print('heylà')
                print(best_server[0])
                file_out.write('{}\n'.format(best_server[0]))

        else:
            params = line.split(';')
            server_ip = params[0]
            bandwidth = float(params[2].split('\n')[0])
            if(server_ip not in servers):
                servers[server_ip] = [0, 0]
            servers[server_ip][0] = servers[server_ip][0] + bandwidth #sommiamo le bdw
            servers[server_ip][1] = servers[server_ip][1] + 1 #aumentiamo il numero di client



def find_best_server(servers):
    best_bandwidth = 0
    for server in servers:
        bandwidth = calculate_avg_bandwidth(servers[server][0],servers[server][1])
        if(bandwidth > best_bandwidth):
            best_bandwidth = bandwidth
            best_server = server
    return [best_server, best_bandwidth]


def calculate_avg_bandwidth(bandwidth, clients_n):
    return bandwidth/clients_n


if __name__ == "__main__":
    monitoring()
