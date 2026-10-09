""""
Programın amacı:
-Bir IPv4 adresini hedef olarak alır.
-Belirlenen TCP portlarını tarar.
-Açık olan portları listeler.
-Açık portların bilinen servis adarını gösterir.
-İstenirse temel banner bilgisi toplamaya çalışır.
-Birden fazla portu aynı anda taramak için thread kullanır.
-Sonuçları TXT,JSON ve CVE olarak kaydedebilir.

KULLANIMI:
python3 NetworkScanner.py -t 127.0.0.1 -p 22,80,443,221

Port aralığı eklenebilir:
python3 NetworkScanner.py -t 127.0.0.1 -p 1-1000

Banner:
python3 NetworkScanner.py -t 127.0.0.1 -p 1-1000 --banner

"""

import socket
#ag baglantilari olusturmak icin kullanilir.
import argparse
#komut satiri argumanlarini almak icin kullanilir.
import threading
import time
import json
import csv
import logging
#log mesajlari olusturmak icin kullanilir.
import ipaddress
import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
#birden fazla portu paralel taramak icin kullanilir.
import shlex
from banner import *

Services={
21: "FTP",
22: "SSH",
23: "Telnet",
25: "SMTP",
53: "DNS",
69: "TFTP",
80: "HTTP",
88: "Kerberos",
110: "POP3",
111: "RPCbind",
119: "NNTP",
123: "NTP",
135: "MS-RPC",
137: "NetBIOS-NS",
138: "NetBIOS-DGM",
139: "NetBIOS-SSN",
143: "IMAP",
161: "SNMP",
389: "LDAP",
443: "HTTPS",
445: "SMB",
465: "SMTPS",
500: "IKE",
514: "Syslog",
587: "SMTP-Submission",
631: "IPP",
636: "LDAPS",
873: "Rsync",
902: "VMware",
993: "IMAPS",
995: "POP3S",
1080: "SOCKS",
1433: "MSSQL",
1521: "Oracle",
2049: "NFS",
2181: "ZooKeeper",
2375: "Docker",
2376: "Docker-TLS",
3000: "Node.js/HTTP",
3306: "MySQL",
3389: "RDP",
4000: "HTTP-Alt",
5000: "HTTP-Alt",
5432: "PostgreSQL",
5601: "Kibana",
5900: "VNC",
5985: "WinRM-HTTP",
5986: "WinRM-HTTPS",
6379: "Redis",
6443: "Kubernetes-API",
8000: "HTTP-Alt",
8008: "HTTP-Alt",
8080: "HTTP-Proxy/Alt-HTTP",
8081: "HTTP-Alt",
8088: "HTTP-Alt",
8443: "HTTPS-Alt",
8888: "HTTP-Alt",
9000: "HTTP-Alt",
9090: "Prometheus/HTTP-Alt",
9200: "Elasticsearch",
9300: "Elasticsearch",
11211: "Memcached",
27017: "MongoDB",
50000: "SAP",
}
DEFAULT_TIMEOUT = 0.5
DEFAULT_WORKERS = 100

MAX_BANNER_LENGTH = 1024
#Programin calisma sirasinda bilgi vermesi icin logger kullaniyorum.

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

thread_local=threading.local()

def validate_target(target):
#girilen hedefin gercek IPv4 adresi olup olmadigini kontrol eder.
    try:
        ip= ipaddress.ip_address(target)
        if ip.version != 4:
            raise ValueError(
                "Only IPv4 is supported."
            )
        return True
    except ValueError:
        return False    

def reverse_dns(target):
#ip adresinden hostname bulmaya calisir.                 
    try:
        hostname=socket.gethostbyaddr(target)[0]
        return hostname
    except socket.herror:
        return None
    except socket.gaierror:
        return None
    except Exception:
        return None
    
def get_service_name(port):
    #port numarasina gore servis adi dondurur.
    if port in Services:
        return Services[port] 
    try:
        service = socket.getservbyport(
            port,
            "tcp"
        )  
        return service
    except OSError:
        return "Unknown"
    
def grab_banner(target,port,timeout):
    #Acik porttan temel banner bilgisi almaya calisir.
    sock = None
    try:
        sock=socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )    
        sock.settimeout(timeout)
        result = sock.connect_ex(
            (target,port)
        )
        
        if result != 0:
            return None
        if port in [
            80,
            3000,
            4000,
            5000,
            8000,
            8008,
            8080,
            8081,
            8088,
            8888,
            9000,
        ]:
            request = (
                "HEAD / HTTP/1.0\r\n"
                f"Host: {target}\r\n"
                "Connection: close\r\n"
                "\r\n"
            )
            sock.sendall(
                request.encode()
            )
        elif port in [
            443,
            8443,
        ]:
            return "HTTPS service detected"    
        else:
            try:
                sock.sendall(
                    b"\r\n"
                )
            except Exception:
                pass
        data = sock.recv(
            MAX_BANNER_LENGTH
        )

        if not data:

            return None

        banner = data.decode(
            "utf-8",
            errors="replace"
        ).strip()

        if not banner:

            return None

        return banner

    except socket.timeout:

        return None

    except ConnectionResetError:

        return None

    except ConnectionRefusedError:

        return None

    except Exception:

        return None

    finally:

        if sock is not None:

            sock.close()    
            
#Tek port tarama            
def scan_port(
    target,
    port,
    timeout,
    banner=False
):
    sock=None
    try:
        sock=socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        sock.settimeout(timeout)
        result=sock.connect_ex(
            (target,port)
        )
        if result ==0:
            service = get_service_name(
                port
            )
            result_data={
               "port": port,
               "state":"open",
               "service":service,
               "banner":None
            }
            if banner:
                result_data["banner"]=grab_banner(
                    target,
                    port,
                    timeout
                )
            return result_data
        return{
            "port": port,

            "state": "closed",

            "service": None,

            "banner": None
        }
    except socket.timeout:
        return{
            "port": port,

            "state": "filtered/timeout",

            "service": None,

            "banner": None
        }    
    except Exception as error:
        return{
            "port": port,

            "state": "error",

            "service": None,

            "banner": str(error)
        }  
    finally:
        if sock is not None:
            sock.close()
            
#port string parser(kullanicinin verdigi port listesini gercek port listesinde ceviriyor.)            
def parse_ports(port_string):
    ports=set()
    #kume kullanmamin sebebi tekrari onlemek
    ports_string = port_string.strip()
    #strip stringin basini ve sonunu temizler.

    if port_string =="-":
        return list(
            range(1,65536)
        )
                 
    parts = port_string.split(",")
    for part in parts:
        part = part.strip()
        if not part :
            continue
        if "-" in part:
            try:
                start, end = part.split("-", 1)  
                start = int (start.strip())  
                end = int(end.strip())
                if start > end :
                    raise ValueError("Port range is invalid.")
                if(start < 1 or end > 65535):
                    raise ValueError("Ports must be between 1 and 65535.")
                for port in range(start,end+1):
                    ports.add(port)  
            except ValueError as error:
                raise ValueError(f"Port range is invalid:{part}") from error
        else:
            try:
                port = int(part)
                if (port<1 or port> 65535):
                    raise ValueError("Ports must be between 1 and 65535.")
                ports.add(port)
            except ValueError as error:
                raise ValueError(f"Invalid port:{part}") 
    return sorted(ports)     
#paralel port baglama
def scan_ports(
    target,
    ports,
    timeout,
    workers,
    banner=False
):
    results = []
    with ThreadPoolExecutor(max_workers=workers)as executor:
        future_to_port = {}
        for port in ports:
            future=executor.submit(scan_port,target,port,timeout,banner)
            future_to_port[future]=port
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                result = future.result()
                results.append(result) 
            except Exception as error:
                logger.error(f"Error while scanning port{port}: {error}")
    results.sort(key=lambda item: item["port"]) 
    return results                    

def print_results(target,hostname,results,elapsed):
    print()
    print(
        BRIGHT_CYAN + "=" * 70 + RESET
    )
    print( BRIGHT_GREEN + "NETWORK SCAN RESULT" + RESET)
    print(f"Target : {target}")
    if hostname:
        print(f"Hostname : {hostname}")
    else:
        print("Hostname : Not Found!")
    print(f"Scan time: {elapsed:.2f} seconds")
    print("-"*70)        
    
    open_ports=[
        result
        for result in results
        if result["state"]== "open"
    ]
    if not open_ports:
        print("No open port was found")
    else:    
        print(
            f"{'PORT':<8}"
            f"{'STATE':<18}"
            f"{'SERVICE':<25}"
        )
        print("-"*70)
        for result in open_ports:
            print(
                f"{result['port']:<8}"
                f"{result['state']:<18}"
                f"{str(result['service']):<25}"
            )
            if result.get("banner"):
                banner = result["banner"]
                banner=banner.replace( "\r"," ").replace("\n"," ")
                print(f"              Banner: {banner[:150]}")
                print("-",*70)
                print(f"Total ports scanned :{len(results)}")
                print(f"open ports : {len(open_ports)}")
                print(BRIGHT_CYAN + "=" *70 + RESET)
                print()
#TXT raporu
def save_txt(
    filename,
    target,
    hostname,
    results,
    elapsed
):
    with open(filename,"w",encoding="utf-8")as file:
        file.write("NETWORK SACNNER REPORT\n")
        file.write("=" * 60 + "\n")
        file.write(f"Target: {target}\n")
        file.write(f"Hostname: {hostname or 'Not Found'}\n")
        file.write(f"Scan time: {elapsed:.2f} seconds\n")
        file.write("="*60 + "\n\n")
        for result in results:
            file.write(f"Port: {result ['port']}\n")
            file.write(f"State: {result ['service']}\n")
            file.write(f"Banner: {result['banner']}\n")
            file.write(f"-"*60 + "\n")
#JSON raporu

def save_json(filename,target,hostname,results,elapsed):
    open_ports =[
        result
        for result in results
        if result ["state"]=="open"
    ]                      
    report ={"target": target,
             "hostname": hostname,
             "scan_time_seconds":round(elapsed,2),
             "total_ports": len(results),
             "open_ports": len(open_ports),
             "results": results
             }
    with open(filename,"w",encoding="utf-8")as file:
        json.dump(report,file,indent=4,ensure_ascii=False)
      
         
#CSV raporu
def save_csv(
    filename,
    results
):
    fieldnames=[
        "port",
        "state",
        "service",
        "banner"
    ]
    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    )as file:
        writer=csv.DictWriter(file,
                              fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writenow(result)
        
#kullanicidan gelen komut seceneklerini hazirliyorum.
def create_argument_parser():
    parser=argparse.ArgumentParser(
        description=("NST - Educational TCP Network Scanner")
    )
    parser.add_argument(
        "-t",
        "--target",
        required=True,
        help=("Target IPv4 address.")
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=("Timeout for each connection "
             "(default: 0.5)"
    )
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=("Number of threads to run concurrently "
              "(default: 100)")
    )
    parser.add_argument(
        "--banner",
        action="store_true",
        help=("Try to get the base banner from open ports.")
    )
    parser.add_argument(
        "--json",
        metavar="FILE",
        help=("Save the results to a JSON file.")
    )
    parser.add_argument(
        "--csv",
        metavar="FILE",
        help=("Save the results to a CSV file.")
    )
    parser.add_argument(
        "--txt",
        metavar="FILE",
        help=("Save the results to a TXT file.")
    )
    parser.add_argument(
    "-p",
    "--ports",
    default="1-1000",
    help="Ports to scan (e.g. 22,80,443 or 1-1000)."
)
    return parser
#scan calistirma
def run_scan(args):
    if not validate_target(args.target):
        print_error(f"Invalid IPv4 address:{args.target}")
        return
    if args.timeout <= 0:
        print_error("Timeout must be greater than 0.")
        return
    if args.workers <= 0:
        print_error("Worker number must be bigger than 0.")
        return
    try:
        ports = parse_ports(args.ports)
    except ValueError as error:
        print_error(str(error))
        return
    if not ports:
        print_error("No ports found to scan.")
        return
    
    
    start_time = time.perf_counter()
    print_section("NETWORK SCANNER")
    print(f"Target: {args.target}")
    print(f"Ports : {len(ports)}")
    print(f"Workers : {args.workers}")
    print(f"Timeout : {args.timeout}")
    print(f"Banner: {'ON' if args.banner else 'OF'}")
    
    print()
    
    #Reverse DNS
    print_info("Checking Reverse DNS record...")
    hostname=reverse_dns(args.target)
    if hostname:
        print.success(f"Hostname: {hostname}")
    else:
        print_warning(f"Hostname not found.")
    print()
    print_info("Starting port scan...")    
    print(f"{BRIGHT_BLACK}"
          F"Scanning {len(ports)} ports..."
          f"{RESET}")
    results =scan_ports(
        target=args.target,
        ports=ports,
        timeout=args.timeout,
        workers=args.workers,
        banner=args.banner
    )
    elapsed=(time.perf_counter()-start_time)
    print_results(
        target=args.target,
        hostname=hostname,
        results=results,
        elapsed=elapsed
    )
    if args.txt:
        save_txt(
            filename=args.txt,
            target=args.target,
            hostname=hostname,
            results=results,
            elapsed=elapsed
        )
        print_success(f"TXT report saved: {args.txt}")
    if args.json:

        save_json(
            filename=args.json,
            target=args.target,
            hostname=hostname,
            results=results,
            elapsed=elapsed )
        print_success(f"JSON report saved: {args.json}")
    
    if args.csv:
        save_csv(
            filename=args.csv,
            results=results
        )        
        print_success(f"CSV report saved: {args.csv}")
        print()
        
#kullanicinin terminal ile etkilesimi
def interactive_scan(command):
    try:
        parts=shlex.split(
            command
        )        
    except ValueError as error:
        print_error(f"Failed to parse command: {error}")
        return
    #scani cikartiyorum
    if parts and parts[0].lower() == "scan":

        parts = parts[1:]  
    if not parts:

        print_error(
            "Usage: scan <IP> [options]"
        )  
        return   
        
#gercek comman-line satiri
    argy =[
        "-t",
        parts[0]
    ]   
    argy.extend(parts[1:])
    parser = create_argument_parser()
    
    try:
        args=parser.parse_args(argy)
    except SystemExit:
        return
    run_scan(args)    
    
    #port listesi
def show_common_ports():
    print_section("COMMON PORTS")
    print( f"{'PORT':<8}{'SERVICE':<30}")   
    print("-*40")
    for port in sorted(Services) :
        print(
            f"{port:<8}"
            f"{Services[port]:<30}"
        )

    print()
    
#yeni banner
def display_new__banner():
    show_banner()
#comand loop
def command_loop():
    while True:
        try:
            command=input(get_prompt()).strip()
        except KeyboardInterrupt:
            print()
            show_exit_message()
            break
        except EOFError:
            print()
            show_exit_message()
            break
        if not command:
            continue
        command_lower=command.lower()
#help   

        if command_lower=="help":
            show_help()
#clear  
        elif command_lower=="banner":
            display_new__banner()
#ports
        elif command_lower=="ports":
            show_common_ports()
#exit
        elif command_lower in ["exit","quit"]:
            show_exit_message()
            break
#scan
        elif command_lower == "scan":
            print_error("Usage: scan <IP> [options]")
            print_info("Example: scan 127.0.0.1 -p 1-1000")
        elif command_lower.startswith("scan"):
            interactive_scan(command)
#unknown 
        else:
            print_error(f"Unknown command: {command}")
#interactive mode terminali baslatir
def interactive_mode():
    show_banner()
    time.sleep(1)
    show_messages()
    time.sleep(0.5)
    show_help()
    time.sleep(0.5)
    command_loop()
#main
def main():
    import sys
    if len(sys.argv)>1:
        parser=create_argument_parser()
        args=parser.parse_args()
        run_scan()
        return
    interactive_mode()  
    # program baslangici
if __name__ == "__main__":

    main()
          
    
                       
                        
        
    
        
        