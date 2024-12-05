# main.py

import readline
from blockbreaker.handler import CommandHandler
from colorama import Fore, init
import os

# Initialize colorama
init(autoreset=True)

# ASCII art for the shell prompt
ascii_art = """
██████╗ ██╗      ██████╗  ██████╗██╗  ██╗██████╗ ██████╗ ███████╗ █████╗ ██╗  ██╗███████╗██████╗ 
██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██║ ██╔╝██╔════╝██╔══██╗
██████╔╝██║     ██║   ██║██║     █████╔╝ ██████╔╝██████╔╝█████╗  ███████║█████╔╝ █████╗  ██████╔╝
██╔══██╗██║     ██║   ██║██║     ██╔═██╗ ██╔══██╗██╔══██╗██╔══╝  ██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗
██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗██████╔╝██║  ██║███████╗██║  ██║██║  ██╗███████╗██║  ██║
╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                                                                                           
"""

def get_username():
    """Retrieve the username for display in the prompt."""
    # Try to get the username from environment variables
    username = os.getenv("USER") or os.getenv("USERNAME") or "user"
    return username

def start_shell():
    """Start the interactive shell loop with colorized output."""
    try:
        print(Fore.CYAN + ascii_art)
        print(Fore.YELLOW + "Welcome to the Minecraft Pentesting Shell. Type 'exit' to quit.")

        handler = CommandHandler()

        # Enable history in the shell, which allows command history using the arrow keys.
        readline.set_history_length(100)  # Set the number of commands to remember in history.

        username = get_username()

        while True:
            # Customize the prompt: username@blockbreaker#
            user_prompt = f"{Fore.GREEN}{username}{Fore.WHITE}@{Fore.BLUE}blockbreaker{Fore.WHITE}#{Fore.RESET} "

            # Simulate a shell prompt with custom design
            try:
                user_input = input(user_prompt).strip()  # Input will now work with arrow keys for navigation
            except EOFError:
                # Handle Ctrl+D (EOFError)
                print(Fore.RED + "\nShell exited with Ctrl+D (EOF).")
                break

            # Split the command and its arguments
            parts = user_input.split()
            command = parts[0]
            args = parts[1:]

            # Execute the command via the handler
            handler.execute(command, args)

    except KeyboardInterrupt:
        # Catch Ctrl+C (KeyboardInterrupt) and exit gracefully
        print(Fore.RED + "\nShell interrupted, exiting...")
    
    except Exception as e:
        # Catch any other unexpected errors
        print(Fore.RED + f"An unexpected error occurred: {str(e)}")
    
    finally:
        # Ensure cleanup, if any, before exiting
        print(Fore.RED + "Shutting down the shell...")

if __name__ == "__main__":
    start_shell()
