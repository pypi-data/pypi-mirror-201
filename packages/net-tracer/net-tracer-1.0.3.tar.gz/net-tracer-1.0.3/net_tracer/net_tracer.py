import argparse
import concurrent.futures
import json
import os
import socket
from datetime import datetime

import nmap
import pyfiglet


# cool banner
banner = pyfiglet.figlet_format("Net Tracer")
print(banner)


def tracer(target=None, ports=None, socket_threads=10000, nmap_threads=8, output=None):
    if not target:
        target = input("Enter target IP address or hostname: ")

    output_file = f"{target}.json" if not output else output

    ports_to_scan = ports if ports else range(1, 65536)

    print(f"\nScanning Target: {target}")
    print(f"Scanning Ports: {ports_to_scan}\nOutput: {output_file}")
    print(f"Start Time: {datetime.now()}")
    print("-" * 50)

    with concurrent.futures.ThreadPoolExecutor(max_workers=socket_threads) as socket_executor:
        open_ports = list(filter(None, socket_executor.map(_scan_open_port, ports_to_scan, [target]*len(ports_to_scan))))

    print(f"\nOpen ports: {open_ports}\n")

    all_port_data = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=nmap_threads) as nmap_executor:
        nmap_executor.map(_scan_port, open_ports, [all_port_data] * len(open_ports), [target] * len(open_ports))

    with open(output_file, "w") as f:
        json.dump(all_port_data, f)

    print(f"\nPort scan results saved to: \n\t{os.path.abspath(output_file)}\n")

    return all_port_data


def _scan_open_port(port, target):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        if sock.connect_ex((target, port)) == 0:
            return port


def _scan_port(port, all_port_data, target):
    try:
        nm = nmap.PortScanner()
        nm.scan(target, str(port))
        state = nm[target]['tcp'][port]['state']
        name = nm[target]['tcp'][port]['name']
        product = nm[target]['tcp'][port]['product']
        version = nm[target]['tcp'][port]['version']
        port_data = {
            "port": port,
            "name": name,
            "state": state,
            "product": product,
            "version": version,
        }
        all_port_data.append(port_data)
        print(f"Port {port} ({name}) is {state} ({product}, {version}).")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")


if __name__ == '__main__':
    tracer()
