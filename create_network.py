from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.node import RemoteController
from mininet.util import irange,dumpNodeConnections

sleep_time = 20    # seconds between client iperf requests


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
    net.pingAll()
    h1, h2, h3, h4 = net.get('h1', 'h2', 'h3', 'h4')
    h1.cmd('./iperfServer.sh {} &'.format(sleep_time))
    h2.cmd('./iperfClient.sh {} &'.format(sleep_time))
    h3.cmd('./iperfClient.sh {} &'.format(sleep_time))
    h4.cmd('./iperfClient.sh {} &'.format(sleep_time))
    CLI(net)

        

    

if __name__ == '__main__':
    build()