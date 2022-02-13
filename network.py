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

conf = config.get_conf("config/network.conf")
sleep_time = conf["sleep_time"]    # seconds between client iperf requests
server_addr_file = conf["server_addr_file"]
current_server_address = conf["server_address"]

class SimpleTopo(Topo):
    "Simple topology of n hosts attached to a switch."
    def __init__(self, n=4, **opts):
        super(SimpleTopo, self).__init__(**opts)
        self.n = n
        switch = self.addSwitch('s1')
        for i in irange(1, n):
            host = self.addHost('h%s' % i, cpu=.5/n)
            # 10 Mbps, 5ms delay, 1% loss, 1000 packet queue
            if(i%2==0):
                self.addLink(host, switch, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
            else:
                self.addLink(host, switch, bw=2, delay='10ms', loss=1, max_queue_size=1000, use_htb=True)


def build():
    topo = SimpleTopo(n=4)
    c = RemoteController('c', '0.0.0.0', 6633)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=None)
    net.addController(c)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    # net.pingAll()
    h1, h2, h3, h4 = net.get('h1', 'h2', 'h3', 'h4')
    # h1.cmd("./loop.sh&")
    h1.cmd('./iperfServer.sh {} &'.format(sleep_time))
    h2.cmd('./iperfClient.sh {} &'.format(sleep_time))
    h3.cmd('./iperfClient.sh {} &'.format(sleep_time))
    h4.cmd('./iperfClient.sh {} &'.format(sleep_time))
    # CLI(net)

    # h1.cmd("taskkill /IM iperfServer.sh")


def monitor_migration_request():
    global current_server_address
    address_file = open(server_addr_file)

    line = address_file.readline()

    print("Checking for migration requests...")

    while True:
        file_server_address = line.split(";")[0].strip()

        if(current_server_address != file_server_address):
            print("Service migration from " + current_server_address + " to " + file_server_address)

            current_server_address = file_server_address

        time.sleep(int(sleep_time))

    address_file.close()


def write_server_address(status="down"):
    file_out = open(server_addr_file, "w")

    file_out.write(current_server_address + ";" + status)

    file_out.close()


if __name__ == '__main__':
    write_server_address()
    
    build()

    write_server_address("up")

    # monitor_migration_request()
