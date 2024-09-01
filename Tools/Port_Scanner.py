import socket
from concurrent.futures import ThreadPoolExecutor
import time
from urllib.parse import urlparse

def extract_hostname(url):
    parsed = urlparse(url)
    return parsed.hostname or parsed.path

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"
            return port, True, service
        else:
            return port, False, None
    except:
        return port, False, None
    finally:
        sock.close()

def scan_ports(ip, num_threads=100):
    start_port = int(input("Enter the starting port: "))
    end_port = int(input("Enter the ending port: "))
    print(f"Scanning {ip} from port {start_port} to {end_port}")
    start_time = time.time()
    
    open_ports = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in range(start_port, end_port + 1)]
        for future in futures:
            port, is_open, service = future.result()
            if is_open:
                open_ports.append((port, service))
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\nScan completed!")
    print(f"Time taken: {duration:.2f} seconds")
    print(f"Open ports: {len(open_ports)}")
    
    if open_ports:
        print("\nPort\tService")
        print("-" * 20)
        for port, service in sorted(open_ports):
            print(f"{port}\t{service}")

def run_port_scanner(url):
    print("Port Scanner")
    try:
        hostname = extract_hostname(url)
        if not hostname:
            print("Invalid input. Please enter a valid hostname or IP address.")
            return

        ip = socket.gethostbyname(hostname)
        scan_ports(ip)
    except socket.gaierror:
        print(f"Hostname '{hostname}' could not be resolved. Please try again.")
    except socket.error:
        print(f"Couldn't connect to server '{hostname}'. Please try again.")
    except ValueError:
        print("Invalid port number. Please enter a valid integer.")
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
