#!/usr/bin/env python3
"""
 ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗███╗   ███╗ █████╗ ██████╗ 
 ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║████╗ ████║██╔══██╗██╔══██╗
 ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║██╔████╔██║███████║██████╔╝
 ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║██║╚██╔╝██║██╔══██║██╔═══╝ 
 ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚═╝ ██║██║  ██║██║     
 ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     
                                          by Sipar Security | v1.0 Free
"""

import argparse
import re
import socket
import sys
import warnings

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from subdomain_enum import enumerate_subdomains
from port_scanner   import scan_subdomains
from dns_recon      import run_dns_recon

console = Console()


def banner():
    console.print(Panel(
        Text(__doc__, style="bold cyan"),
        border_style="cyan",
        padding=(0, 2)
    ))


def parse_args():
    parser = argparse.ArgumentParser(
        description="ShadowMap Free — Web Reconnaissance Tool by Sipar Security",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py --domain example.com
  python3 main.py --domain example.com --skip-ports

Upgrade to ShadowMap Pro for:
  - Active subdomain brute-force with SecLists
  - Technology fingerprinting
  - Misconfiguration & vulnerability detection
  - Stealth modes
  - Professional HTML/PDF report generation
  - JSON export

  --> siparsecurity.github.io

For authorized testing only. Always have written permission.
        """
    )
    parser.add_argument("--domain",     required=True,       help="Target domain (e.g. example.com)")
    parser.add_argument("--skip-dns",   action="store_true", help="Skip DNS recon & zone transfer")
    parser.add_argument("--skip-ports", action="store_true", help="Skip port scanning")
    return parser.parse_args()


def print_config(args, domain):
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold dim")
    table.add_column(style="cyan")
    table.add_row("Target",  domain)
    table.add_row("Edition", "Free")
    console.print(table)
    console.print()


def validate_domain(domain: str) -> bool:
    """Return True if domain looks like a valid hostname."""
    if not domain:
        return False
    # Basic pattern: labels separated by dots, each label alphanumeric + hyphens
    pattern = r'^(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$'
    return bool(re.match(pattern, domain))


def main():
    banner()
    args = parse_args()
    domain = args.domain.lower().strip()

    if not validate_domain(domain):
        console.print(f"[bold red][!] Invalid domain: '{domain}'. Please provide a valid hostname (e.g. example.com)[/bold red]")
        sys.exit(1)

    print_config(args, domain)

    # DNS Recon
    dns_results = {}
    if not args.skip_dns:
        dns_results = run_dns_recon(domain)
        leaked = dns_results.get("zone_transfer", {}).get("leaked_hosts", [])
        if leaked:
            console.print(f"[bold red][!!!] {len(leaked)} hosts leaked via zone transfer[/bold red]")
    else:
        console.print("[yellow][!] DNS recon skipped.[/yellow]")

    # Subdomain Enumeration — passive only
    subdomains = enumerate_subdomains(domain)

    if dns_results:
        leaked_hosts = dns_results.get("zone_transfer", {}).get("leaked_hosts", [])
        existing = {e["subdomain"] for e in subdomains}
        for host in leaked_hosts:
            if host not in existing:
                try:
                    ip = socket.gethostbyname(host)
                    subdomains.append({"subdomain": host, "ip": ip})
                    existing.add(host)
                except socket.gaierror:
                    pass

    if not subdomains:
        console.print("[yellow][!] No live subdomains found. Exiting.[/yellow]")
        sys.exit(0)

    # Port Scan — top 20 ports only
    scan_results = {}
    if not args.skip_ports:
        scan_results = scan_subdomains(subdomains, use_nmap=False)
    else:
        console.print("[yellow][!] Port scanning skipped.[/yellow]")
        for entry in subdomains:
            scan_results[entry["subdomain"]] = {"ip": entry["ip"], "ports": []}

    # Print results to terminal
    console.print("\n[bold green]✅ ShadowMap Free — Scan Complete[/bold green]\n")

    console.print(f"[bold]Subdomains found:[/bold] {len(subdomains)}")
    for s in subdomains:
        ports = scan_results.get(s["subdomain"], {}).get("ports", [])
        port_str = ", ".join(str(p["port"]) for p in ports) if ports else "none"
        console.print(f"  [cyan]{s['subdomain']}[/cyan] ({s['ip']}) — ports: {port_str}")

    console.print("\n[dim]Want technology fingerprinting, vuln detection, and PDF reports?[/dim]")
    console.print("[dim]Upgrade to ShadowMap Pro → siparsecurity.github.io[/dim]\n")
    console.print("[dim]For authorized testing only. Sipar Security.[/dim]\n")


if __name__ == "__main__":
    main()