from ping3 import ping
from scan_utils import scan_network, scan_and_label


DEVICES = scan_and_label()

def check_devices():
    results = {}
    for name, ip in DEVICES.items():
        latency = ping(ip, timeout=1)
        results[name] = {
            "ip": ip,
            "latency_ms": round(latency * 1000, 1) if latency else None,
            "state": latency is not None
        }
    return results
