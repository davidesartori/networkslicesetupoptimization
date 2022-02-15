"""
Author: Gruppo 22 Networking II
Description: Implementation of network monitoring
"""

#from re import I
import time
import modules.config as config
import modules.logger as logger


def write_server_address(server_address):
    conf = config.get_conf("config/monitoring.conf")
    server_log = conf["server_addr_file"]
    file_out = open(server_log, "w")
    file_out.write(server_address)
    file_out.close()


def monitoring():
    conf = config.get_conf("config/monitoring.conf")
    threshold = int(conf["threshold"])
    iperf_log = conf["iperf_file"]
    log_file = conf["log_file"]
    wait = int(conf['sleep_time'])
    CURRENT_BANDWIDTH = -1

    logger.log(log_file, "Monitoring initialized")

    #{ip_server: [bandwidth, client_counter]}
    servers = {}
    while True:
        file_in = open(iperf_log, 'r')
        Lines = file_in.readlines()
        file_in.close()
        for line in Lines:
            if('#' in line):
                if(len(servers)==1):
                    server = list(servers)[0]
                    current_bdw = calculate_avg_bandwidth(servers[server][0], servers[server][1])
                    print('current bandwidth: {}'.format(current_bdw))
                    if(CURRENT_BANDWIDTH == -1):
                        CURRENT_BANDWIDTH = current_bdw
                    else:
                        if(current_bdw > CURRENT_BANDWIDTH):
                            CURRENT_BANDWIDTH = current_bdw
                    if((current_bdw-CURRENT_BANDWIDTH+threshold) < 0):
                        logger.log(log_file, "Bandwidth below threshold detected, asking for migration")
                        print('bandwidth dropped below threshold')
                        write_server_address('migrate')
                else:
                    logger.log(log_file, "Finding the best server")
                    best_server = find_best_server(servers)
                    CURRENT_BANDWIDTH = best_server[1]
                    write_server_address(best_server[0])
                    print('best server is {}'.format(best_server[0]))
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
        time.sleep(wait)


def find_best_server(servers):
    best_bandwidth = -1
    best_server = 'none'
    for server in servers:
        bandwidth = calculate_avg_bandwidth(servers[server][0],servers[server][1])
        if(bandwidth > best_bandwidth):
            best_bandwidth = bandwidth
            best_server = server
    return [best_server, best_bandwidth]


def calculate_avg_bandwidth(bandwidth, clients_n):
    return bandwidth/clients_n


if __name__ == '__main__':
    conf = config.get_conf('config/monitoring.conf')
    wait = int(conf['sleep_time'])
    time.sleep(wait) # Give time to network.py to execute iperf
    monitoring()
