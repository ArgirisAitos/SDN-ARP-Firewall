from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel

class MyTopo(Topo):
    def build(self):
        switch = self.addSwitch('s1')
       
       # set a static ARP table to map IP addresses to MAC addresses
        hosts = {
            'h1': ('10.0.0.1', '52:a2:b2:97:17:c8'),
            'h2': ('10.0.0.2', '42:96:15:ec:4f:2f'),
            'h3': ('10.0.0.3', '42:fd:3e:81:6e:3c'),
            'h4': ('10.0.0.4', '46:4f:66:a6:98:72')
        }
for h, (ip, mac) in hosts.items():
            host = self.addHost(h, ip=ip, mac=mac)
            self.addLink(host, switch)

if __name__ == '__main__':
    setLogLevel('info')
    topo = MyTopo()
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()

    CLI(net)
    net.stop()
