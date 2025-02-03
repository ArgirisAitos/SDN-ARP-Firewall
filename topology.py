from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, arp

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
       
        self.arp_table = {}
        self.arp_table = {
            '10.0.0.1': '52:a2:b2:97:17:c8',
            '10.0.0.2': '42:96:15:ec:4f:2f',
            '10.0.0.3': '42:fd:3e:81:6e:3c',
            '10.0.0.4': '7e:86:c9:34:71:a4'
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
