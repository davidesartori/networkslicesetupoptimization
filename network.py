"""
Author: Gruppo 22 Networking II
Description: Implementation of an SDN
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.util import irange,dumpNodeConnections
import modules.config as config
import os
import time


class SimpleTopo(Topo):
    "Simple topology of n hosts attached to a switch."
    def __init__(self, n=4, **opts):
        super(SimpleTopo, self).__init__(**opts)
        self.n = n
        host_config = dict(inNamespace=True)
        switch_link_config = dict(bw=1)
        host_link_config = dict()

        for i in range(4):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig)

        for i in range(4):
            self.addHost("h%d" % (i + 1), **host_config)

        self.addLink("s1", "s2", **switch_link_config)
        self.addLink("s2", "s4", **switch_link_config)
        self.addLink("s1", "s3", **switch_link_config)
        self.addLink("s3", "s4", **switch_link_config)

        self.addLink("h1", "s1", **host_link_config)
        self.addLink("h2", "s1", **host_link_config)
        self.addLink("h3", "s4", **host_link_config)
        self.addLink("h4", "s4", **host_link_config)


def build(net):
    c = RemoteController("c", ip="127.0.0.1", port=6633)
    net.addController(c)
    net.build()
    net.start()
    print("Testing network connectivity")
    # net.pingAll()
    h1, h2, h3, h4 = net.get('h1', 'h2', 'h3', 'h4')
    # h1.cmd('./iperfServer.sh {} &'.format(sleep_time))
    # h2.cmd('./iperfClient.sh {} &'.format(sleep_time))
    # h3.cmd('./iperfClient.sh {} &'.format(sleep_time))
    # h4.cmd('./iperfClient.sh {} &'.format(sleep_time))
    # CLI(net)


def execute_iperf(hosts, current_server, current_server_address):
    iperf_string = ""

    for host in hosts:
        h = net.get(host)
        s = net.get(current_server)

        s.cmd("iperf -s -p 5566&")
        iperf_output = h.cmd("iperf -c " + current_server_address + " -p 5566")
        if(iperf_output[0] == "-"):
            bandwidth = float(iperf_output.split("\n")[6].split(" ")[-2].split(" ")[0])
            udm = iperf_output.split("\n")[6].split(" ")[-1].split(" ")[0].strip()
        else:
            bandwidth = 0
            udm = 'N'

        if(udm[0] == 'M'):
            bandwidth *= 1000
        elif(udm[0] == 'G'):
            bandwidth *= 10000001

        iperf_string += current_server + ";" + host + ";" + str(bandwidth) + "\n"

    return iperf_string


def execute_iperf_for_migration(hosts, servers):
    iperf_string = ""

    for server in servers:

        s = net.get(server)

        for host in hosts:
            h = net.get(host)

            s.cmd("iperf -s -p 5566&")
            server_address = "10.0.0." + server[1:]
            iperf_output = h.cmd("iperf -c " + server_address + " -p 5566")

            if(iperf_output[0] == "-"):
                bandwidth = iperf_output.split("\n")[6].split("  ")[4].split(" ")[0]
            else:
                bandwidth = "0"

            iperf_string += server_address + ";" + host + ";" + bandwidth + "\n"

    return iperf_string


def write_server_address(current_server_address):
    file_out = open(server_addr_file, "w")
    file_out.write(current_server_address)
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
    net = net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )

    build(net)

    while True:
        file_address = get_current_server_address(server_addr_file)

        if file_address == current_server_address:
            print("Running iperf to check current server performance")
            iperf_result = execute_iperf(hosts, current_server, current_server_address)
            iperf_result = iperf_result[:-1]
            print("Performance analysis done")
            write_iperf(iperf_file, iperf_result)
        elif file_address == "migrate":
            print("Executing iperf on every server")
            iperf_result = execute_iperf_for_migration(hosts, servers)
            write_iperf(iperf_file, iperf_result[:-1])

            while file_address == "migrate":
                file_address = get_current_server_address(server_addr_file)
                time.sleep(10)
        else:
            print("migrate the service")
            current_server = "h" + file_address.split(".")[-1]

        time.sleep(int(sleep_time))
