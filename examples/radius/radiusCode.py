#!/usr/bin/python

'This example shows how to work with Radius Server'

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mininet.wifi.node import UserAP
from mininet.wifi.cli import CLI_wifi
from mininet.wifi.net import Mininet_wifi


def topology():
    "Create a network."
    net = Mininet_wifi( controller=Controller, accessPoint=UserAP,
                   enable_wmediumd=True, enable_interference=True )

    info("*** Creating nodes\n")
    sta1 = net.addStation( 'sta1', radius_passwd='sdnteam', encrypt='wpa2',
                           radius_identity='joe', position='110,120,0' )
    sta2 = net.addStation( 'sta2', radius_passwd='hello', encrypt='wpa2',
                           radius_identity='bob', position='200,100,0' )
    ap1 = net.addAccessPoint( 'ap1', ssid='simplewifi', authmode='8021x',
                              mode='a', channel='36', encrypt='wpa2', position='150,100,0' )
    c0 = net.addController('c0', controller=Controller, ip='127.0.0.1', port=6633 )

    info("*** Configuring Propagation Model\n")
    net.propagationModel(model="logDistance", exp=3.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating Stations\n")
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)

    net.plotGraph(max_x=300, max_y=300)

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start( [c0] )

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
