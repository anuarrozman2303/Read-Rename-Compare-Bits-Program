import configparser
import argparse
import os

# Load config.ini
config = configparser.ConfigParser()
config.read('C:/Python/IR Compare/Daikin/Commands/config.ini')

# Get the available commands from the config.ini file
available_commands = [option for option in config.options('command files')]

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Rename input file based on command')

# Add a command line argument for the command
parser.add_argument('--command', type=str, help='Command to rename the input file')

# Parse the command line arguments
args = parser.parse_args()

# Check if the entered command is valid
command = args.command
if command in available_commands:
    # Call the rename_input_file() function with the specified command
    rename_input_file(command)
else:
    print(f"Error: '{command}' is not a valid command.")
