from scapy.all import ARP, Ether, srp

KNOWN_MACS = {
    "6C:4B:90:55:8E:90": "Kali",
    "74:56:3c:f6:f4:81": "Main pc",
    "58:25:75:af:39:41": "Router",
    "6c:99:9d:3d:4f:07": "FireTVStick",
    "74:ec:b2:49:35:82": "Echo Dot",
    "a2:2a:4e:22:76:11": "IPhone 11",
    "d4:a6:51:7a:00:ad": "LED Strip"
}

def scan_network(subnet="192.168.1.0/24"):
    arp_request = ARP(pdst=subnet)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    answered, unanswered = srp(packet, inter=0.05, timeout=2, verbose=0)

    devices = []
    for sent, received in answered:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc
        })

    return devices

def scan_and_label():
    devices = scan_network()
    labeled = {}
    for device in devices:
        mac = device["mac"]
        name = KNOWN_MACS.get(mac, mac)
        labeled[name] = device["ip"]
    return labeled


if __name__ == "__main__":
    for device in scan_network():
        print(device)