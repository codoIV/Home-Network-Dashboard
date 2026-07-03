# Home Network Dashboard

A small Flask web app that discovers devices on your local network via ARP scanning, checks their live status with ICMP pings, and displays everything on an auto-refreshing dashboard.

Built as a personal tool to keep an eye on what's connected at home — and as a hands-on project to learn about network discovery, Flask, and dynamic frontend rendering.

![dashboard preview](https://github.com/codoIV/Home-Network-Dashboard/blob/main/HomeNetworkDashboard.png?raw=true)

## What it does

- **Discovers devices automatically** using an ARP scan of the local subnet — no need to hardcode IPs.
- **Checks live status** (online/offline) and latency for each discovered device via ICMP ping.
- **Labels known devices** with friendly names (e.g. "Router", "Main pc") based on their MAC address, and falls back to showing the raw MAC for anything unrecognized.
- **Auto-refreshes** in the browser every few seconds via polling — no page reload needed.

## Why ARP scanning + MAC-based labels?

Devices on a network can change IP address over time (via DHCP), but their MAC address stays the same. Instead of hardcoding IPs, this project scans the whole subnet for any device that responds to ARP, then matches known MAC addresses to friendly names in a small local lookup table. Any device not in that table still shows up — just labeled with its MAC address instead of a name — so nothing on the network goes unnoticed.

Note: a device can show up in the scan (meaning it's on the network) but still show as "offline" in the ping check. This isn't a bug — some devices block or rate-limit ICMP pings even while fully connected. The dashboard reports two related but different things: *presence* (ARP) and *reachability* (ping).

## Requirements

- Python 3.8+
- Root/admin privileges (required for raw packet access used by the ARP scan)
- A machine connected to the local network you want to scan

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/codoIV/home-network-dashboard.git
   cd home-network-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your subnet**

   Open `scan_utils.py` and check the `subnet` default matches your network (most home networks use `192.168.1.0/24` or `192.168.0.0/24`). You can check your own subnet by running `ipconfig` (Windows) or `ip a` (Linux) and looking at your local IP.

4. **Run the app** (needs root privileges for the ARP scan)
   ```bash
   sudo python3 app.py
   ```

5. **Open the dashboard**

   Visit `http://127.0.0.1:5000` in your browser.

## Labeling your own devices

On first run, every device will show up labeled with its raw MAC address, since none are recognized yet. To give your devices friendly names:

1. Run the app once and note the MAC addresses shown on the dashboard (or run `python3 scan_utils.py` directly to print raw scan results to the console).
2. Figure out which MAC belongs to which device. A few ways to do this:
   - Check your router's admin page — most list connected devices with both MAC address and device hostname.
   - Look up the MAC's OUI (first 6 characters) online to identify the manufacturer as a hint.
   - Turn a device's WiFi off/on and see which entry disappears/reappears from the scan.
   - Check the device's own network settings, which usually show its MAC address directly.
3. Open `scan_utils.py` and add each MAC/name pair to the `KNOWN_MACS` dictionary:
   ```python
   KNOWN_MACS = {
       "aa:bb:cc:dd:ee:ff": "Router",
       "11:22:33:44:55:66": "Main PC",
   }
   ```
4. Restart the app — labeled devices will now show their friendly name instead of their MAC address.

## Project structure

```
home-network-dashboard/
├── app.py              # Flask app and routes
├── ping_utils.py        # Builds device dict, checks online status + latency
├── scan_utils.py         # ARP network scan + MAC-to-name labeling
├── templates/
│   └── index.html         # Page template
├── static/
│   ├── script.js            # Fetches status, renders table, auto-refresh
│   └── style.css             # Table styling + animated status dots
└── requirements.txt
```

## Known limitations

- The machine running the scan won't see itself in the results — this is expected ARP behavior (a host doesn't reply to its own ARP broadcast).
- Only discovers devices on the same local subnet as the scanning machine.
- Requires root/admin privileges due to raw packet access — this is a scapy requirement, not something the app can avoid.
- `KNOWN_MACS` is manually maintained; there's currently no auto-detection of device type or hostname.

## Ethical note

This tool sends ARP requests across the local subnet to discover connected devices. Only run it on networks you own or have explicit permission to scan.

## Possible future improvements

- Auto-detect the local subnet instead of hardcoding it.
- Persist discovered devices in a small database instead of memory.
- Desktop/browser notifications when a device goes offline.
- Optional hostname resolution as a fallback label.
