# Importing necessary modules
import concurrent.futures             # For concurrent execution of threads
import os                             # For operating system related functionality
import socket                         # For creating socket objects for port scanning
from datetime import datetime         # For printing the current date and time
import csv                            # For writing data to csv file
import string                         # For special valid characters in output filename
import importlib                      # For checking if nmap is installed


# Make sure pyfiglet and nmap are installed
try:
    importlib.import_module('pyfiglet')
    importlib.import_module('nmap')
except ImportError as e:
    if str(e) == "No module named 'pyfiglet'":
        if str(e) == "No module named 'nmap'":
            print("Error: Both pyfiglet and nmap modules are not installed. Please install them using 'pip install pyfiglet python-nmap' and try again.")
        else:
            print("Error: The pyfiglet module is not installed. Please install it using 'pip install pyfiglet' and try again.")
    elif str(e) == "No module named 'nmap'":
        print("Error: The nmap module is not installed. Please install it using 'pip install python-nmap' and try again.")
    os.sys.exit()


from nmap import PortScanner          # For scanning ports using Nmap
import pyfiglet                       # For Net Tracer banner when printing 

def banner():
    # cool banner
    os.system("cls")
    print("-"*79 + "\n")
    banner = pyfiglet.figlet_format((" "*16 + "Net Tracer"))
    print(banner)
    print("-"*79 + "\n")


# Define a function to scan the specified ports on the target host
def tracer(target=None, ports=None, socket_threads=10000, nmap_threads=8, output=None, printing=False):

    # Prompt user to enter target IP address or hostname
    if not target:
        os.system("cls")
        banner() # Print Net Tracer banner
        target = input("Please enter the target IP address or hostname: ")
        # Prompt user to enter ports to scan
        while True:
            try:
                banner()
                print(f"\tTarget:".ljust(25), "|", f"\t{target}\n")
                ports_input = input("Please enter the ports you would like to scan (e.g. 80, 443, 22), or press Enter to scan all ports: ")
                print("\n" + "-"*79)
                
                if ports_input.startswith("[") and ports_input.endswith("]"):
                    # Handle input format [80, 443, 22]
                    ports_input = ports_input[1:-1]
                
                # Split the ports by comma or space and convert to integers
                ports = [int(port_str.strip()) for port_str in ports_input.replace(",", " ").split()]
                
                if len(ports) == 0:
                    ports = range(1, 62535)
                
                break

            except ValueError:
                print("Invalid input. Please enter a list of port numbers separated by commas or spaces.")

        # Prompt user to enter number of socket threads
        while True:
            try:
                banner()
                print("--- Each thread runs at the same time making it scan multiple ports at once --- \n")
                print("-"*79 + "\n")
                print(f"\tTarget:".ljust(25), "|", f"\t{target}")
                print(f"\tPorts:".ljust(25), "|", f"\t{ports}\n")
                socket_threads_input = input("Please enter the number of socket threads to use (default 10000): ")
                socket_threads = int(socket_threads_input) if socket_threads_input else 10000
                break
                
            except ValueError:
                print("Invalid input. Please enter an integer value.")
        
        # Prompt user to enter number of Nmap threads
        while True:
            try:
                banner()
                print("--- Each thread runs at the same time making it scan multiple ports at once --- \n")
                print("-"*79 + "\n")
                print(f"\tTarget:".ljust(25), "|", f"\t{target}")
                print(f"\tPorts:".ljust(25), "|", f"\t{ports}")
                print(f"\tSocket Threads:".ljust(25), "|", f"\t{socket_threads}\n")
                nmap_threads_input = input("Please enter the number of Nmap threads to use (default 8): ")
                print("\n" + "-"*79)
                nmap_threads = int(nmap_threads_input) if nmap_threads_input else 8
                break
                
            except ValueError:
                print("Invalid input. Please enter an integer value.")
        
        # Prompt user to enter output filename
        while True:
            try:
                banner()
                print(f"\tTarget:".ljust(25), "|", f"\t{target}")
                print(f"\tPorts:".ljust(25), "|", f"\t{ports}")
                print(f"\tSocket Threads:".ljust(25), "|", f"\t{socket_threads}")
                print(f"\tNmap Threads:".ljust(25), "|", f"\t{nmap_threads}\n")
                output = str(input("\nPlease enter the output filename (press Enter to skip): "))
                
                # Check if file extension is .csv and add it if not present
                if output and not output.endswith(".csv"):
                    output += ".csv"

                break
                
            except Exception as e:
                print(f"Input Error: {e}")
        
        # Prompt user to choose whether to print results to console
        while True:
            try:
                banner()
                print(f"\tTarget:".ljust(25), "|", f"\t{target}")
                print(f"\tPorts:".ljust(25), "|", f"\t{ports}")
                print(f"\tSocket Threads:".ljust(25), "|", f"\t{socket_threads}")
                print(f"\tNmap Threads:".ljust(25), "|", f"\t{nmap_threads}")
                print(f"\tOutput Filename:".ljust(25), "|", f"\t{output}") if output else None
                print("\n" + "-"*79)
                printing_input = input("\nDo you want to print results to console? (y/n): ")
                printing = printing_input.lower() == "y"
                break
                
            except ValueError:
                print("Invalid input. Please enter 'y' or 'n'.")

        
    if output:
        # Set the output file
        output_file = format_filename(output) # replaces invalid characters with underscores
    else:
        # Set the output file to `None` if not specified
        output_file = None
            
    
    # If ports are not specified, scan all ports from 1 to 65535
    ports_to_scan = ports or range(1, 65536)

    # Print the details of the scan
    if printing:
        banner() # Print Net Tracer banner
        target_label = "\tScanning Target:"
        ports_label = "\tScanning Ports:"
        output_label = "\tOutput:"
        start_label = "\tStart Time:"
        separator_text = " | "

        print(f"{target_label:<25}{separator_text}\t{target}")
        print(f"{ports_label:<25}{separator_text}\t{ports_to_scan}")
        print(f"{output_label:<25}{separator_text}\t{output_file}") if output_file else None
        print(f"\n{start_label:<25}{separator_text}\t{datetime.now()}\n")
        print("-" * 79)

    # Scan the open ports using threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=socket_threads) as socket_executor:
        # Filter out the None values returned by the _scan_open_port() function
        open_ports = list(filter(None, socket_executor.map(_scan_open_port, ports_to_scan, [target]*len(ports_to_scan))))

    # Print the list of open ports
    if printing:
        open_ports_label = "\tOpen ports:"
        separator_text = " | "

        print(f"\n{open_ports_label:<25}{separator_text}\t{open_ports}\n")

    # Create a list to store the port data
    all_port_data = []

    # Scan each open port using Nmap
    with concurrent.futures.ThreadPoolExecutor(max_workers=nmap_threads) as nmap_executor:
        # Pass the same arguments to _scan_port() for each port
        nmap_executor.map(_scan_port, open_ports, [all_port_data] * len(open_ports), [target] * len(open_ports), [printing] * len(open_ports))

    # Simply aesthetic, prints a newline after displaying last port information
    if printing:
        print("\n" + "-"*79 + "\n")

    # Write the port scan data to a CSV file
    if output_file:
        with open(output_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["port", "name", "state", "product", "version"])
            writer.writeheader()
            for port_data in all_port_data:
                writer.writerow(port_data)
        # Print the path of the output file
        if printing:
            print(f"\tPort scan results saved to: \n\t\t{os.path.abspath(output_file)}\n")
            print("-"*79 + "\n")
    
    # Return the list of port data
    return all_port_data


# Define a function to scan an individual port and return the port number if it is open
def _scan_open_port(port, target):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex((target, port)) == 0:
                return port
    except Exception as e:
        print(f"Socket Error (scanning for open ports): {e}")

# Define a function to scan an individual port using Nmap
def _scan_port(port, all_port_data, target, printing):
    try:
        nm = PortScanner()
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
        # Append the port data to the all_port_data
        all_port_data.append(port_data)
        if printing:
            
            which_port = f"\tPort {port} ({name}):"
            port_info = f"\t({product}, {version})"
            separator_text = " | "

            print(f"{which_port:<25}{separator_text}{port_info}")

    except Exception as e:
        if printing:
            print(f"Nmap Error scanning port {port}: {e}")


# Remove and replace any invalid characters in the filename with underscores
def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c if c in valid_chars else '_' for c in s)


if __name__ == '__main__':
    tracer()
