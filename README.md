# Network Scanner

A lightweight TCP network scanner built with Python.

Network Scanner is a command-line tool. I developed to explore network communication, TCP port scanning, and service identification. It scans a target IPv4 address, identifies open TCP ports, and optionally attempts to retrieve basic service information.

The project combines multithreaded scanning with an interactive terminal interface and support for exporting scan results.


<p align="center">
  <img src="network_scanner.png" alt="Network Scanner terminal interface" width="850">
</p>

## Features

- **TCP Port Scanning** — Scan individual ports, multiple ports, or a specified port range.
- **Multithreading** — Scan multiple ports concurrently using Python's `ThreadPoolExecutor`.
- **Service Identification** — Display common service names associated with TCP port numbers.
- **Banner Grabbing** — Attempt to retrieve basic information from services running on open ports.
- **Reverse DNS Lookup** — Attempt to resolve an IPv4 address to a hostname.
- **Report Generation** — Export scan results to TXT, JSON, and CSV files.
- **Interactive CLI** — Run scans and access commands through a custom terminal interface.
- **Custom Terminal UI** — Colored output, ASCII banners, and status messages.

## Technologies

- Python 3
- TCP/IP
- Socket Programming
- Multithreading
- `concurrent.futures`
- `argparse`
- `ipaddress`
- JSON and CSV

The project uses Python's standard library and does not require third-party packages.


### Requirements

- Python 3
- A terminal or command-line environment

### Installation

Clone the repository:

```bash
git clone https://github.com/suheylanur/network-scanner.git
```

Navigate to the project directory:

```bash
cd network-scanner
```

Start the interactive interface:

```bash
python3 NetworkScanner.py
```

Enter `help` to view the available commands.

#### Scan selected ports

```text
scan 127.0.0.1 -p 22,80,443
```

#### Scan a range of ports

```text
scan 127.0.0.1 -p 1-1000
```

#### Enable banner grabbing

```text
scan 127.0.0.1 -p 22,80,443 --banner
```

#### Save scan results

Save results as a TXT report:

```bash
python3 NetworkScanner.py -t 127.0.0.1 -p 22,80,443 --txt scan-report.txt
```

Save results as a JSON report:

```bash
python3 NetworkScanner.py -t 127.0.0.1 -p 22,80,443 --json scan-report.json
```

Save results as a CSV report:

```bash
python3 NetworkScanner.py -t 127.0.0.1 -p 22,80,443 --csv scan-report.csv
```

## How It Works

1. Validates the target IPv4 address.
2. Parses the specified ports and port ranges.
3. Attempts TCP connections to the selected ports.
4. Uses a thread pool to scan multiple ports concurrently.
5. Identifies common services associated with port numbers.
6. Optionally attempts banner grabbing.
7. Displays the results and saves reports when requested.

## Limitations

- Supports IPv4 targets and TCP port scanning.
- Service identification is based on known port mappings and does not guarantee which service is actually running.
- Banner grabbing is best-effort and may not return information from every service.
- A timeout or filtered connection does not necessarily mean a port is closed.
- This project is a network scanning tool, not a complete vulnerability assessment platform.

## Responsible Use

This tool is intended for educational purposes and authorized network testing.

Only scan systems you own or have explicit permission to test.

## Author

Developed as a hands-on project to practice Python programming, TCP networking, multithreading, and command-line application development.
