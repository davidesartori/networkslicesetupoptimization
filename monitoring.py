def start_monitoring():
    file = open('log.txt', 'r')
    Lines = file.readlines()
    #{host: [ip, porta, bandwidth]}
    hosts = {}
    for line in Lines:
        if('[ ID] Interval       Transfer     Bandwidth\n' in line):
            pass
        if('connected with' in line):
            params = line.split('] local 10.0.0.1 port 5566 connected with ')
            id_host = params[0][3]
            host_ip = params[1].split(' port ')[0]
            host_port = params[1].split(' port ')[1].split('\n')[0]
            if(id_host in hosts):
                #la si chiama ogni volta che inizia un nuovo "ciclo"
                #di richieste iperf 
                avg = calculate_avg_bandwidth(hosts)
                #pulisco per inserire i valori del nuovo "ciclo"
                print(avg)
                hosts = {}
            hosts[id_host] = [host_ip, host_port]
        if('Bytes   ' in line):
            params = line.split('Bytes   ')
            bandwidth = int(params[1].split('\n')[0].split(' ')[0])
            id_host = params[0].split(']  ')[0][3]
            hosts[id_host].append(bandwidth)



def calculate_avg_bandwidth(hosts):
    number_hosts = len(hosts)
    bandwidth = 0
    for host in hosts:
        bandwidth += hosts[host][2]
    avg = bandwidth / number_hosts
    return avg


if __name__ == "__main__":
    start_monitoring()
