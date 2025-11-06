import argparse
from modules import crtsh, dir_enum, port_scanner, whois_lookup

command_functions ={
    "crtsh": crtsh.search_crt,
    "dir_enum": dir_enum.directory_enumeration,
    "port_scan": port_scanner.port_scan,
    "whois": whois_lookup.buscar_whois
}

def main():
    parser = argparse.ArgumentParser(description="Network Scanner Tool", epilog="Example: python main.py crtsh example.com")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    #CRTSH Command
    parser_crtsh = subparsers.add_parser("crtsh", help="Search for certificates")
    parser_crtsh.add_argument("target", help="Target domain")

    # Directory Enumaration Command
    parser_dir_enum = subparsers.add_parser("dir_enum", help="Directory enumeration")
    parser_dir_enum.add_argument("target", help="Target domain")
    parser_dir_enum.add_argument("wordlist", help="Path to wordlist file")

    #Port Scanner Command
    parser_port_scan = subparsers.add_parser("port_scan", help="Port scanner")
    parser_port_scan.add_argument("target", help="Target IP or hostname")
    parser_port_scan.add_argument("ports", nargs="+", type=int, help="Ports to scan")

    #WhoIS Command
    parser_whois = subparsers.add_parser("whois", help="Whois lookup")
    parser_whois.add_argument("domain", help="Domain to lookup")

    args = parser.parse_args()

    if args.command in command_functions:
        func = command_functions[args.command]
        if args.command == "port_scan":
            results = func(args.target, args.ports)
        elif args.command == "dir_enum":
            results = func(args.target, args.wordlist)
        else:
            results = func(args.target)
        print(f"Results for {args.command}:") if results else print(f"No results found for {args.command}.")
        [print(result) for result in results] if results else None
    else:
        parser.print_help()

if __name__ == "__main__":
    main()