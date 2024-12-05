import hashlib
import requests
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def get_offline_player(username):
    """Fetch UUID for offline players (cracked accounts)."""
    h = hashlib.md5(f"OfflinePlayer:{username}".encode()).hexdigest()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"

def get_premium_player(username):
    """Fetch UUID for premium players (Minecraft official accounts)."""
    try:
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        if response.status_code == 200:
            return response.json()["id"]
        else:
            return None
    except requests.RequestException as e:
        print(Fore.RED + f"Error fetching premium UUID: {e}")
        return None

def get_bedrock_player(xbox_id):
    """Fetch UUID for Bedrock players using their Xbox ID via playerdb.co."""
    try:
        response = requests.get(f"https://playerdb.co/api/player/xbox/{xbox_id}")
        if response.status_code == 200:
            data = response.json()
            if data["data"]:
                return data["data"]["player"]["id"]
            else:
                return None
        else:
            return None
    except requests.RequestException as e:
        print(Fore.RED + f"Error fetching Bedrock UUID: {e}")
        return None

def format_uuid(uuid):
    """Format UUID to the xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx format."""
    return f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"

def get_trimmed_uuid(uuid):
    """Return the UUID without hyphens."""
    return uuid.replace("-", "")

def fetch_uuid(username, platform):
    """Fetch UUID based on platform."""
    if platform.lower() == "java":
        # Fetch premium UUID
        premium_uuid = get_premium_player(username)
        
        # Display premium UUID or a message if not found
        if premium_uuid:
            formatted_premium_uuid = format_uuid(premium_uuid)
            trimmed_premium_uuid = get_trimmed_uuid(premium_uuid)
            print(Fore.GREEN + f"Premium (Online) UUID for {username}: {formatted_premium_uuid} ({trimmed_premium_uuid})")
        else:
            print(Fore.RED + f"No premium ID found for {username}.")
        
        # Fetch and display cracked (offline) UUID in light red
        offline_uuid = get_offline_player(username)
        trimmed_offline_uuid = get_trimmed_uuid(offline_uuid)
        print(Fore.LIGHTRED_EX + f"Cracked (Offline) UUID for {username}: {offline_uuid} ({trimmed_offline_uuid})")

    elif platform.lower() == "bedrock":
        bedrock_uuid = get_bedrock_player(username)
        if bedrock_uuid:
            print(Fore.CYAN + f"Bedrock (Xbox) UUID for {username}: {bedrock_uuid} ({get_trimmed_uuid(bedrock_uuid)})")
        else:
            print(Fore.RED + f"Could not find Bedrock UUID for {username}.")
    else:
        print(Fore.RED + "Invalid platform specified. Please use 'java' or 'bedrock'.")

def main():
    """Main function to handle input and display UUID."""
    if len(sys.argv) != 3:
        print(Fore.RED + "Usage: python uuid.py <username> <platform>")
        print(Fore.RED + "Platform: 'java' or 'bedrock'")
        sys.exit(1)

    username = sys.argv[1]
    platform = sys.argv[2]

    fetch_uuid(username, platform)

if __name__ == "__main__":
    main()
