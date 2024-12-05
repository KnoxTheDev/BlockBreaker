# clear.py

from colorama import Fore
import os

# ASCII art for the shell prompt
ascii_art = """
██████╗ ██╗      ██████╗  ██████╗██╗  ██╗██████╗ ██████╗ ███████╗ █████╗ ██╗  ██╗███████╗██████╗ 
██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██║ ██╔╝██╔════╝██╔══██╗
██████╔╝██║     ██║   ██║██║     █████╔╝ ██████╔╝██████╔╝█████╗  ███████║█████╔╝ █████╗  ██████╔╝
██╔══██╗██║     ██║   ██║██║     ██╔═██╗ ██╔══██╗██╔══██╗██╔══╝  ██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗
██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗██████╔╝██║  ██║███████╗██║  ██║██║  ██╗███████╗██║  ██║
╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                                                                         
"""

def clear_command(args=None):
    """Clears the terminal screen and prints the ASCII art."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Windows uses 'cls', other OS uses 'clear'
    print(Fore.CYAN + ascii_art)  # Print the ASCII art again
    print("Screen cleared.")
