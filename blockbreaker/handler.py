# handler.py

from blockbreaker.commands.server import server_command
from blockbreaker.commands.exit import exit_shell
from blockbreaker.commands.clear import clear_command  # Import the clear command
from blockbreaker.commands.uuid import fetch_uuid  # Import the fetch_uuid function for UUID fetching
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

class CommandHandler:
    """Handles the routing of commands to their respective functions."""
    
    def __init__(self):
        # Define available commands and their corresponding functions
        self.commands = {
            'server': server_command,
            'help': self.display_help,
            'exit': exit_shell,  # Add exit command to the list
            'clear': clear_command,  # Add clear command to the list
            'uuid': self.fetch_uuid_handler  # Add the uuid command handler function
        }
        # Define help descriptions for each command
        self.command_help = {
            'server': 'Ping the Minecraft server for additional details.',
            'help': 'Display help information for commands.',
            'exit': 'Exit the Minecraft Pentesting Shell.',
            'clear': 'Clear the terminal screen.',
            'uuid': 'Fetch the UUID of a Minecraft player (java or bedrock).'  # Add uuid description
        }

    def execute(self, command, args):
        """Executes the given command with its arguments."""
        if command in self.commands:
            print(Fore.CYAN + f"Executing command: {command} with arguments: {args}")
            self.commands[command](args)
        else:
            # Use red color for unknown commands
            print(Fore.RED + f"Unknown command: {command}")
            self.display_help()  # Display the list of available commands

    def fetch_uuid_handler(self, args):
        """Handles the UUID fetching command by passing the correct arguments to fetch_uuid."""
        if len(args) != 2:
            print(Fore.RED + "Usage: uuid <username> <java/bedrock>")
            return
        username = args[0]
        platform = args[1].lower()  # Ensure platform is in lowercase

        # Call the fetch_uuid function with the correct arguments
        fetch_uuid(username, platform)

    def display_help(self, args=None):
        """Display help for a specific command or all commands."""
        if not args:  # If no command is specified, show all commands
            print(Fore.YELLOW + "Available commands:")
            for cmd in self.commands:
                print(Fore.GREEN + f"- {cmd}: {self.command_help[cmd]}")
        else:  # If a specific command is provided, show its help
            command = args[0].lower()
            if command in self.command_help:
                print(Fore.YELLOW + f"{Fore.GREEN}{command}{Fore.YELLOW}: {self.command_help[command]}")
            else:
                print(Fore.RED + f"Unknown command for help: {command}")
                self.display_help()  # Show general help if command not found
