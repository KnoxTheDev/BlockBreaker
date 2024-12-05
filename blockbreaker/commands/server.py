from mcstatus import JavaServer, BedrockServer
from colorama import Fore, Style, init
import re
import socket
import dns.resolver

# Initialize colorama
init(autoreset=True)

def server_command(args):
    """Pings the Minecraft server at the given IP and port using mcstatus and adds color."""
    
    if len(args) != 2:
        print(Fore.RED + "Usage: server <server_ip[:server_port]> <java/bedrock>")
        return

    server_info = args[0]  # The server IP or domain (may include a port)
    server_type = args[1].lower()  # Get the server type: java or bedrock

    # Try to split the domain/host:port if present
    if ":" in server_info:
        server_ip, server_port = server_info.split(":")
        try:
            server_port = int(server_port)  # Ensure the port is an integer
        except ValueError:
            print(Fore.RED + "Please provide a valid server port (integer).")
            return
    else:
        server_ip = server_info
        server_port = None  # No port provided, we will try to resolve the port

    # Try to resolve domain to an IP if it's a domain name (e.g., "boomjava.shockbyte.pro")
    if not is_valid_ip(server_ip):
        try:
            # First, attempt to fetch SRV records if the domain is not an IP
            server_ip, server_port = get_srv_record(server_ip, server_type) if server_port is None else (server_ip, server_port)
        except Exception as e:
            print(Fore.RED + f"Could not resolve domain or SRV record error: {e}")
            return

    print(Fore.CYAN + f"Pinging Minecraft {server_type.capitalize()} server at {server_ip}...")

    try:
        if server_type == "java":
            if server_port is not None:
                server = JavaServer(server_ip, server_port)  # Use JavaServer for Java Edition
                status = server.status()  # Sends a ping request to the server
            else:
                server = JavaServer(server_ip)  # Just pass the IP (no port)
                status = server.status()  # Sends a ping request to the server
        elif server_type == "bedrock":
            if server_port is not None:
                server = BedrockServer(server_ip, server_port)  # Use BedrockServer for Bedrock Edition
                status = server.status()  # Sends a ping request to the server
            else:
                server = BedrockServer(server_ip)  # Just pass the IP (no port)
                status = server.status()  # Sends a ping request to the server
        else:
            print(Fore.RED + "Invalid server type. Please specify 'java' or 'bedrock'.")
            return

        print(Fore.GREEN + f"Successfully connected to {server_ip}!")

        # Remove decimal precision from ping
        ping = int(status.latency)  # Truncate decimal part
        print(Fore.YELLOW + f"Ping: {ping}ms")  # Display ping as integer
        
        # Print Server Version and protocol
        print(Fore.MAGENTA + f"Server Version: {status.version.name}")  # Server Version version info
        print(Fore.MAGENTA + f"Server Protocol: {status.version.protocol}")  # Print server protocol
        
        # Print MOTD (Message of the Day) with color processing
        if server_type == "java":
            motd = status.description
            # Check for plugins attribute before accessing
            if hasattr(status, 'plugins'):
                plugins = status.plugins  # Get the list of plugins installed on the server
                if plugins:
                    print(Fore.BLUE + f"Plugins/Mods: {', '.join(plugins)}")
                else:
                    print(Fore.BLUE + "No mods found/installed.")
            else:
                print(Fore.BLUE + "Plugins information not available.")
        elif server_type == "bedrock":
            motd = status.motd.raw  # Use the raw MOTD for Bedrock

        # Process MOTD for color codes
        motd = process_motd(motd)
        print(Fore.CYAN + f"MOTD: {motd}")
        
        print(Fore.YELLOW + f"Players online: {status.players.online}/{status.players.max}")
        
        # Player list
        if server_type == "java":
            player_list = status.players.sample  # Get a list of online players
            if player_list:
                print(Fore.GREEN + "Online Players: " + ", ".join([process_motd(player.name) for player in player_list]))
            else:
                print(Fore.GREEN + "Online Players: None")

    except Exception as e:
        print(Fore.RED + f"Error while pinging server: {e}")
        print(Fore.RED + f"Failed to connect to {server_ip}.")

def get_srv_record(domain, server_type):
    """Fetches the SRV record for a Minecraft server (Java or Bedrock)."""
    try:
        # Minecraft SRV record prefixes
        service = "_minecraft"  # Standard for both versions
        protocol = "_tcp" if server_type == "java" else "_udp"  # Java uses TCP, Bedrock uses UDP

        # Query DNS SRV records for the domain
        answers = dns.resolver.resolve(f"{service}.{protocol}.{domain}", "SRV")
        for rdata in answers:
            target = str(rdata.target).rstrip('.')
            port = rdata.port
            print(Fore.GREEN + f"Found SRV record: {target}:{port}")
            return target, port  # Return resolved target and port
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN) as e:
        print(Fore.RED + f"No SRV record found for {domain} or invalid domain.")
        raise e

def process_motd(motd):
    """Process the MOTD to handle color codes."""
    # Check if the MOTD is a string or not
    if isinstance(motd, str):
        return apply_color_codes(motd)
    else:
        # If MOTD is an object (for example, Bedrock), convert to string and apply color codes
        return apply_color_codes(str(motd))

def apply_color_codes(motd):
    """Apply Minecraft color codes (§) to the MOTD using colorama."""
    # Use regex to replace Minecraft color codes with the corresponding colorama codes
    # Example: §c -> Fore.RED
    motd = re.sub(r'§([0-9a-fk-or])', lambda match: color_code_to_fore(match.group(1)), motd)
    return motd

def color_code_to_fore(code):
    """Convert Minecraft color code to colorama Fore color."""
    color_map = {
        '0': Fore.BLACK,
        '1': Fore.BLUE,
        '2': Fore.GREEN,
        '3': Fore.CYAN,
        '4': Fore.RED,
        '5': Fore.MAGENTA,
        '6': Fore.YELLOW,
        '7': Fore.WHITE,
        '8': Fore.BLACK,
        '9': Fore.BLUE,
        'a': Fore.GREEN,
        'b': Fore.CYAN,
        'c': Fore.RED,
        'd': Fore.MAGENTA,
        'e': Fore.YELLOW,
        'f': Fore.WHITE,
        'k': Style.BRIGHT,    # Random
        'l': Style.BRIGHT,    # Bold
        'm': Style.DIM,       # Strikethrough
        'n': Style.NORMAL,    # Underline
        'o': Style.NORMAL,    # Italic
        'r': Style.RESET_ALL  # Reset
    }
    return color_map.get(code, "")

def is_valid_ip(ip):
    """Check if the given string is a valid IP address."""
    try:
        socket.inet_aton(ip)  # This will throw an error if it's not a valid IP
        return True
    except socket.error:
        return False
