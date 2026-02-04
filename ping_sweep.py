import subprocess
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
import time
import platform

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def ping_host(ip):
    # Cross platform ping command
    system = platform.system()   
    if system == "Windows":
        cmd = ["ping", "-n", "1", "-w", "1000", ip]
    else:
        cmd = ["ping", "-c", "1", "-W", "1000", ip]
    
    try:
        res = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2
        )
        return ip if res.returncode == 0 else None
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None

def ping_sweep():
    local_ip = get_local_ip()
    network_prefix = ".".join(local_ip.split(".")[:3]) + "."

    print(f"\nLocal IP detected: {local_ip}")
    print(f"Scanning network {network_prefix}0/24\n")

    alive_hosts = []
    total_hosts = 254
    checked = 0

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {
            executor.submit(ping_host, network_prefix + str(i)): i
            for i in range(1, 255)
        }

        for future in as_completed(futures):
            checked += 1
            result = future.result()

            print(f"Progress: {checked}/{total_hosts}", end="\r", flush=True)

            if result:
                print(f"\n[+] {result} is alive")
                alive_hosts.append(result)

    print("\n\nScan complete.")
    print(f"{len(alive_hosts)} host(s) responded.")

    return alive_hosts

if __name__ == "__main__":
    print("Starting...\n")
    time.sleep(2)
    start_time = datetime.datetime.now()
    print(f"Ping sweep started at: {start_time.strftime('%H:%M:%S')}")

    ping_sweep()

    end_time = datetime.datetime.now()
    print(f"Finished at: {end_time.strftime('%H:%M:%S')}\n")

    scan_duration = end_time - start_time
    print(f"Total scan time: {scan_duration.total_seconds():.2f} seconds")

