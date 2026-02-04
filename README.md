# PingSweeper

A fast, concurrent network scanner that discovers active hosts on your local network by performing ping sweeps. PingSweeper automatically detects your local network and scans all 254 addresses in the /24 subnet to identify connected devices.

## Features

- **Automatic Network Detection**: Automatically determines your local IP address and network prefix
- **Concurrent Scanning**: Uses multi-threading (50 concurrent workers) for fast network scans
- **Real-time Progress**: Displays scanning progress and discovers hosts as they respond
- **Efficient**: Only pings each host once with a 1-second timeout
- **Detailed Reporting**: Shows scan duration, number of responsive hosts, and timestamps

## Requirements

- Python 3.6+
- `ping` utility (available by default on Linux, macOS, and Windows)
- Linux or macOS (uses `ping -c` flag for single count)

## Installation

1. Clone or download this repository:
```bash
git clone https://github.com/KeeganMadell/PingSweeper.git
cd PingSweeper
```

2. Ensure the script is executable:
```bash
chmod +x ping_sweep.py
```

## Usage

Run the script with Python:

```bash
python3 ping_sweep.py
```

### Example Output

```
Starting...

Local IP detected: 192.168.1.45
Scanning network 192.168.1.0/24

Progress: 254/254
[+] 192.168.1.1 is alive
[+] 192.168.1.5 is alive
[+] 192.168.1.45 is alive
[+] 192.168.1.100 is alive

Scan complete.
4 host(s) responded.
Ping sweep started at: 14:23:45
Finished at: 14:23:52

Total scan time: 7.34 seconds
```

## How It Works

1. **Network Detection**: Connects to a public DNS server (8.8.8.8) to determine your local IP address
2. **Network Range**: Extracts the first three octets of your IP to determine the network range (e.g., 192.168.1.0/24)
3. **Concurrent Pinging**: Uses ThreadPoolExecutor with 50 workers to ping all 254 addresses (1-254) simultaneously
4. **Results**: Collects and displays responsive hosts with their IP addresses and scan timing

## Performance

- Typical scan time: 5-15 seconds depending on network load
- 50 concurrent workers balance speed with system resource usage
- 1-second timeout per ping prevents hanging on unreachable hosts

## Notes

- This script scans only the local /24 subnet (Class C network)
- Requires appropriate network permissions to send ping requests
- Some networks may have ICMP filtering or rate limiting that affects results
- The script counts IP addresses 1-254, excluding network (0) and broadcast (255) addresses

## Troubleshooting

**"No such file or directory: ping"**: Ensure the `ping` utility is installed and accessible from your system PATH.

**No hosts found**: Check your network connectivity or firewall settings that might block ICMP packets.

**Permission denied**: On some systems, ping requires elevated privileges. Try running with `sudo`.

## License

This project is provided as-is for educational and network diagnostic purposes.
