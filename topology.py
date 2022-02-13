#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
About: Basic example of service (running inside a APPContainer) migration.
"""

from comnetsemu.cli import CLI
from comnetsemu.net import Containernet, VNFManager
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections


if __name__ == "__main__":
    net = Containernet(controller=RemoteController, link=TCLink, xterms=False)
    mgr = VNFManager(net)

    info("*** Add the remote controller\n")
    c = RemoteController('c', '0.0.0.0', 6633)
    net.addController(c)

    info("*** Creating the hosts\n")
    h1 = net.addDockerHost(
        "h1",
        dimage="dev_test",
        ip="10.0.0.1/24",
        docker_args={"hostname": "h1"},
    )
    h2 = net.addDockerHost(
        "h2",
        dimage="dev_test",
        ip="10.0.0.2/24",
        docker_args={"hostname": "h2", "pid_mode": "host"},
    )
    h3 = net.addDockerHost(
        "h3",
        dimage="dev_test",
        ip="10.0.0.3/24",
        docker_args={"hostname": "h3", "pid_mode": "host"},
    )

    info("*** Adding switch and links\n")
    s1 = net.addSwitch("s1")
    # Add the interfaces for service traffic.
    net.addLinkNamedIfce(s1, h1, bw=1000, delay="5ms")
    net.addLinkNamedIfce(s1, h2, bw=1000, delay="5ms")
    net.addLinkNamedIfce(s1, h3, bw=1000, delay="5ms")


    net.addLink(
        s1,
        h1,
        bw=1000,
        delay="1ms",
        intfName1="s1-h1-int",
        intfName2="h1-s1-int",
    )
    net.addLink(
        s1,
        h2,
        bw=1000,
        delay="1ms",
        intfName1="s1-h2-int",
        intfName2="h2-s1-int",
    )
    net.addLink(
        s1,
        h3,
        bw=1000,
        delay="1ms",
        intfName1="s1-h3-int",
        intfName2="h3-s1-int",
    )

    info("*** Deploy service on h1.\n")
    server_h1 = mgr.addContainer(
        "server_h1",
        "h1",
        "service_migration",
        "python3 /home/server.py",
    )

    info("*** Deploy service on h2.\n")
    client_h2 = mgr.addContainer(
        "client_h2",
        "h2",
        "service_migration",
        "python3 /home/client.py",
    )

    info("*** Deploy service on h3.\n")
    client_h3 = mgr.addContainer(
        "client_h3",
        "h3",
        "service_migration",
        "python3 /home/client.py",
    )



    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    CLI(net)
    net.stop()
    mgr.stop()

    
