# exit.py

import sys
import signal
from colorama import Fore

def signal_handler(sig, frame):
    """Handle termination signals (Ctrl+C or system signals)."""
    print(Fore.RED + "\nExiting Minecraft Pentesting Shell due to interrupt...")
    sys.exit(0)

def terminate_on_ctrl_z(sig, frame):
    """Exit the program when Ctrl+Z (SIGTSTP) is pressed."""
    print(Fore.RED + "\nCtrl+Z detected. Exiting the shell...")
    sys.exit(0)

def exit_shell(args=None):
    """Exit the shell when 'exit' command is called."""
    print(Fore.RED + "Exiting Minecraft Pentesting Shell...")
    sys.exit(0)

# Set up signal handling for graceful exit
signal.signal(signal.SIGINT, signal_handler)  # Catch Ctrl+C (SIGINT)
signal.signal(signal.SIGTERM, signal_handler)  # Catch termination signal (SIGTERM)
signal.signal(signal.SIGTSTP, terminate_on_ctrl_z)  # Exit on Ctrl+Z (SIGTSTP)
