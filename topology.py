from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_topology():
    net = Mininet(controller=RemoteController)

    # Add controller
    c0 = net.addController('c0', ip='127.0.0.1', port=6633)

    # Add switch
    s1 = net.addSwitch('s1')

    # Add hosts
    h1 = net.addHost('h1', ip='10.0.0.1')  # authorized
    h2 = net.addHost('h2', ip='10.0.0.2')  # authorized
    h3 = net.addHost('h3', ip='10.0.0.3')  # BLOCKED

    # Add links
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)

    # Start network
    net.start()
    print("\n*** Topology started")
    print("*** h1 (10.0.0.1) - AUTHORIZED")
    print("*** h2 (10.0.0.2) - AUTHORIZED")
    print("*** h3 (10.0.0.3) - BLOCKED\n")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_topology()
