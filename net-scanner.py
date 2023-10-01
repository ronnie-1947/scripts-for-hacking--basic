import scapy.all as scapy
import argparse
import re

def get_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='ip', help='Declare an IP or network range')    
    options = parser.parse_args()

    if not options.ip:
        options.ip = input('Write an ip > ')

    ipv4_pattern = r'^\d{1,3}(\.\d{1,3}){3}(?:/\d{1,2})?$'

    if not (re.match(ipv4_pattern, options.ip)):
        raise ValueError('Invalid ip address')

    return options.ip


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []

    for el in answered:
        dic = {"ip": el[1].psrc, "mac": el[1].hwsrc}
        clients_list.append(dic)

    return clients_list;


def nice_print(client_list):

    print("IP\t\t\tMAC Adress\n----------------------------------------")

    for el in client_list:
        print (f'{el["ip"]}\t\t{el["mac"]}')
    return 


ip = get_args()
list = scan(ip) # '192.168.157.1/24'
nice_print(list)