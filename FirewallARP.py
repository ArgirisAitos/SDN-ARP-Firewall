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

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)



        match = parser.OFPMatch(eth_type=0x0806, ip_proto=1)
        actions = [parser.OFPActionOutput(ofproto.OFPP_NORMAL)]
        self.add_flow(datapath, 10,match,actions)


    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                 match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == 0x0806:  # ARP
            self.handle_arp(datapath, pkt, eth, in_port)

    def handle_arp(self, datapath, pkt, eth, in_port):
        arp_pkt = pkt.get_protocol(arp.arp)
       
        if arp_pkt.opcode == arp.ARP_REQUEST:
            self.logger.info("ARP Request: %s -> %s", arp_pkt.src_ip, arp_pkt.dst_ip)
            
           # Checks the ARP Request for spoofing
            if arp_pkt.src_ip in self.arp_table:
                if self.arp_table[arp_pkt.src_ip] != arp_pkt.src_mac:
                    self.logger.warning("ARP Spoofing detected: %s is claiming %s", arp_pkt.src_mac, arp_pkt.src_ip)
                    return  # decline the packets
            else:
                self.arp_table[arp_pkt.src_ip] = arp_pkt.src_mac

        elif arp_pkt.opcode == arp.ARP_REPLY:
            self.logger.info("ARP Reply: %s -> %s", arp_pkt.src_ip, arp_pkt.dst_ip)
            
             # Checks the ARP reply for spoofing
            if arp_pkt.src_ip in self.arp_table:
                if self.arp_table[arp_pkt.src_ip] != arp_pkt.src_mac:
                    self.logger.warning("ARP Spoofing detected: %s is claiming %s", arp_pkt.src_mac, arp_pkt.src_ip)
                    return  # decline the packets
            else:
                self.arp_table[arp_pkt.src_ip] = arp_pkt.src_mac

        # sent ARP packet if it is not a spoofing packet
        actions = [datapath.ofproto_parser.OFPActionOutput(datapath.ofproto.OFPP_FLOOD)]
        out = datapath.ofproto_parser.OFPPacketOut(datapath=datapath,
                                                   buffer_id=datapath.ofproto.OFP_NO_BUFFER,
                                                   in_port=in_port, actions=actions, data=pkt.data)
        datapath.send_msg(out)
