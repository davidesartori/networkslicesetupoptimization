"""
Author: Gruppo 22 Networking II
Description: Implementation of network monitoring
"""

#from re import I
import time
import modules.config as config
import modules.logger as logger




def monitoring():
    conf = config.get_conf("config/monitoring.conf")
    threshold = int(conf["threshold"])
    server_log = conf["server_addr_file"]
    iperf_log = conf["iperf_file"]
    log_file = conf["log_file"]
    CURRENT_BANDWIDTH = -1

    logger.log(log_file, "Monitoring initialized")

    #{ip_server: [bandwidth, client_counter]}
    servers = {}
    while True:
        file_in = open(iperf_log, 'r')
        file_out = open(server_log, 'w')
        Lines = file_in.readlines()
        for line in Lines:
            print(line)
            if('#' in line):
                if(len(servers)==1):
                    print('ci sta un solo server')
                    server = list(servers)[0]
                    current_bdw = calculate_avg_bandwidth(servers[server][0], servers[server][1])
                    print('bandwidth corrente: {}'.format(current_bdw))
                    if(CURRENT_BANDWIDTH == -1):
                        CURRENT_BANDWIDTH = current_bdw
                    if((current_bdw-CURRENT_BANDWIDTH+threshold) < 0):
                        logger.log(log_file, "Bandwidth below threshold detected, asking for migration")
                        file_out.write('migrate\n')
                        time.sleep(10) # wait for data
                else:
                    logger.log(log_file, "Finding the best server")
                    best_server = find_best_server(servers)
                    CURRENT_BANDWIDTH = best_server[1]
                    print(best_server[0])
                    file_out.write(best_server[0])
                servers = {}

            else:
                params = line.split(';')
                if(params[2] == '0\n'):
                    pass
                else:
                    server_ip = params[0]
                    bandwidth = float(params[2].split('\n')[0])
                    if(server_ip not in servers):
                        servers[server_ip] = [0, 0]
                    servers[server_ip][0] = servers[server_ip][0] + bandwidth #sommiamo le bdw
                    servers[server_ip][1] = servers[server_ip][1] + 1 #aumentiamo il numero di client
        time.sleep(3)


def find_best_server(servers):
    best_bandwidth = -1
    best_server = 'none'
    for server in servers:
        bandwidth = calculate_avg_bandwidth(servers[server][0],servers[server][1])
        if(bandwidth > best_bandwidth):
            best_bandwidth = bandwidth
            best_server = server
    print(best_server)
    print(best_bandwidth)
    return [best_server, best_bandwidth]


def calculate_avg_bandwidth(bandwidth, clients_n):
    return bandwidth/clients_n


if __name__ == "__main__":
    monitoring()
