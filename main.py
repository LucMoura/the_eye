import argparse
from modules import crtsh, dir_enum, port_scanner, whois_lookup

command_functions ={
    "crtsh": crtsh.search_crt,
    "dir_enum": dir_enum.directory_enumeration,
    "port_scan": port_scanner.port_scan,
    "whois": whois_lookup.buscar_whois,
    "geo": whois_lookup.geolocalizar,
}

def main():
    parser = argparse.ArgumentParser(
        description="Network Scanner Tool",
        epilog="Example: python main.py crtsh example.com")

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

    if args.command not in command_functions:
        parser.print_help()
        return

    func = command_functions[args.command]

    try:
        if args.command == "port_scan":
            results = func(args.target, args.ports)
        elif args.command == "dir_enum":
                results = func(args.target, args.wordlist)
        elif args.command in ("whois", "geo"):
             results = func(args.target)
        else:
             results = func(args.target)

        print(f"\n=== Resultados de '{args.command}' ===")
        if not results:
            print("Nenhum resultado encontrado")
            return

        if isinstance (results, dict):
             for key, value in results.items():
                  print(f"{key}: {value}")
        elif isinstance(results, list):
             for item in results:
                print(item)
        else:
             print(results)
            
    except Exception as e:
        print(f"[ERRO] Falha ao executar '{args.command}' : {e}")


if __name__ == "__main__":
    main()