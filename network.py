"""
Author: Gruppo 22 Networking II
Description: Implementation of an SDN
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.node import RemoteController
from mininet.util import irange,dumpNodeConnections
import modules.config as config
import os
import time


class SimpleTopo(Topo):
    "Simple topology of n hosts attached to a switch."
    def __init__(self, n=4, **opts):
        super(SimpleTopo, self).__init__(**opts)
        self.n = n
        switch = self.addSwitch('s1')
        for i in irange(1, n):
            host = self.addHost('h%s' % i, cpu=.5/n)
            # 10 Mbps, 5ms delay, 1% loss, 1000 packet queue
            if i % 2 == 0:
                self.addLink(host, switch, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
            else:
                self.addLink(host, switch, bw=2, delay='10ms', loss=1, max_queue_size=1000, use_htb=True)


def build(net):
    c = RemoteController('c', '0.0.0.0', 6633)

    net.addController(c)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    # net.pingAll()
    h1, h2, h3, h4 = net.get('h1', 'h2', 'h3', 'h4')
    # h1.cmd('./iperfServer.sh {} &'.format(sleep_time))
    # h2.cmd('./iperfClient.sh {} &'.format(sleep_time))
    # h3.cmd('./iperfClient.sh {} &'.format(sleep_time))
    # h4.cmd('./iperfClient.sh {} &'.format(sleep_time))
    # CLI(net)


def execute_iperf(hosts, current_server):
    iperf_string = ""

    for host in hosts:
        h = net.get(host)
        s = net.get(current_server)

        s.cmd("iperf -s -p 5566&")
        iperf_output = h.cmd("iperf -c 10.0.0.1 -p 5566")
        bandwidth = iperf_output.split("\n")[6].split("  ")[4].split(" ")[0]
        iperf_string += current_server + ";" + host + ";" + bandwidth + "\n"

    return iperf_string
    


def write_server_address(current_server_address, status="down"):
    file_out = open(server_addr_file, "w")
    file_out.write(current_server_address + ";" + status)
    file_out.close()


def write_iperf(path, string):
    file_out = open(path, "w")
    file_out.write(string + "\n#\n")
    file_out.close()


def get_current_server_address(path):
    file_in = open(path)
    address = file_in.readline()
    file_in.close()
    address = address.split(";")[0].strip()

    return address



if __name__ == '__main__':
    conf = config.get_conf("config/network.conf")
    sleep_time = conf["sleep_time"]  # seconds between client iperf requests
    server_addr_file = conf["server_addr_file"]
    current_server_address = conf["server_address"]
    iperf_file = conf["iperf_file"]
    hosts = ["h3", "h3"]
    servers = ["h1", "h4"]
    current_server = "h" + current_server_address.split(".")[-1]

    write_server_address(current_server_address)

    topo = SimpleTopo(n=4)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=None)
    build(net)

    write_server_address(current_server_address, "up")

    while True:
        file_address = get_current_server_address(server_addr_file)

        if file_address == current_server_address:
            print("Running iperf to check current server performance")
            iperf_result = execute_iperf(hosts, current_server)
            iperf_result = iperf_result[:-1]
            print("Performance analysis done")
            write_iperf(iperf_file, iperf_result)
        elif file_address == "migrate":
            print("run iperf on all the servers and wait for feedback")
        else:
            print("migrate the service")
            current_server = "h" + file_address.split(".")[-1]

        time.sleep(int(sleep_time))
