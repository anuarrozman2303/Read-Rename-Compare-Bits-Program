import os
import configparser

# Load the config.ini file
config = configparser.ConfigParser()
config.read('C:\\Python\\IR Compare\\Daikin\\Commands\\config.ini')

# Get the default format from config.ini
default_format = config.get('command files', 'default_format')
on_format = config.get('command files', 'on_format')
off_format = config.get('command files', 'off_format')
mode_cold_format = config.get('command files', 'mode_cold_format')
mode_dry_format = config.get('command files', 'mode_dry_format')

# Get the file format mappings from config.ini
file_formats = dict(config.items('command files'))

# Get the input file name from the user
input_file_name = input("Enter the input file name: ")

# Extract the file extension
file_extension = os.path.splitext(input_file_name)[1]

# Get the format for the input file from the config.ini
input_file_format = file_formats.get(input_file_name, on_format)
input_file_format = file_formats.get(input_file_name, off_format)
input_file_format = file_formats.get(input_file_name, mode_cold_format)
input_file_format = file_formats.get(input_file_name, mode_dry_format)

# Generate a formatted file name
formatted_file_name = input_file_format + file_extension

# Get the current directory
current_directory = os.getcwd()

# Provide the full path to the input file
input_file_path = os.path.join(current_directory, input_file_name)

# Provide the full path to the formatted file name
formatted_file_path = os.path.join(current_directory, formatted_file_name)

# Rename the input file
os.rename(input_file_path, formatted_file_path)

print(f"File successfully renamed to '{formatted_file_name}'")
