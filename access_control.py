from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr
from pox.lib.packet.ethernet import ethernet

log = core.getLogger()

WHITELIST = ['10.0.0.1', '10.0.0.2']
BLOCKED   = ['10.0.0.3']

class AccessController(object):

    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)
        self.mac_to_port = {}
        log.info("Switch connected: %s" % dpidToStr(connection.dpid))

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            return

        in_port = event.port

        # Learn MAC to port mapping
        self.mac_to_port[packet.src] = in_port

        # Check if it's an IP packet
        ip = packet.find('ipv4')
        if ip:
            src = str(ip.srcip)
            dst = str(ip.dstip)

            # Block if either src or dst is in blocked list
            if src in BLOCKED or dst in BLOCKED:
                log.info("DROPPING IP packet: %s -> %s" % (src, dst))
                msg = of.ofp_flow_mod()
                msg.priority = 100
                msg.match = of.ofp_match.from_packet(packet, in_port)
                msg.idle_timeout = 30
                # No actions = DROP
                self.connection.send(msg)
                return

            if src in WHITELIST and dst in WHITELIST:
                log.info("ALLOWING IP packet: %s -> %s" % (src, dst))

        # Check ARP - block ARP from/to blocked hosts
        arp = packet.find('arp')
        if arp:
            src_ip = str(arp.protosrc)
            dst_ip = str(arp.protodst)
            if src_ip in BLOCKED or dst_ip in BLOCKED:
                log.info("DROPPING ARP: %s -> %s" % (src_ip, dst_ip))
                return  # Just don't forward, drop silently

        # Forward packet - use learned port or flood
        if packet.dst in self.mac_to_port:
            out_port = self.mac_to_port[packet.dst]

            # Install flow rule for future packets
            msg = of.ofp_flow_mod()
            msg.priority = 10
            msg.match = of.ofp_match.from_packet(packet, in_port)
            msg.idle_timeout = 30
            msg.actions.append(of.ofp_action_output(port=out_port))
            self.connection.send(msg)

            # Forward this packet
            msg2 = of.ofp_packet_out()
            msg2.data = event.ofp
            msg2.in_port = in_port
            msg2.actions.append(of.ofp_action_output(port=out_port))
            self.connection.send(msg2)
        else:
            # Flood if we don't know the port
            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.in_port = in_port
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)

class access_control(object):
    def __init__(self):
        core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        AccessController(event.connection)

def launch():
    core.registerNew(access_control)
    log.info("SDN Access Control launched | Whitelist: %s | Blocked: %s" % (WHITELIST, BLOCKED))
