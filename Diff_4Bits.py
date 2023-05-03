import os
import configparser

# Read the config file
config = configparser.ConfigParser()
config.read('configsample.ini')

def process_file(section_name):
    # Get the filename associated with the given section name
    filename = config.get(section_name, os.name)

    # Open the input file for reading
    with open(filename, 'r') as infile:
        # Read in all the lines of the file
        lines = infile.readlines()

    # Remove everything before the colon, remove all non-numeric characters, and remove empty lines
    lines = [line.split(':', 1)[-1] for line in lines]
    lines = [''.join(c for c in line if c in ['0', '1']) for line in lines]
    lines = [line.strip() for line in lines if line.strip()]

    # Create the output filename
    outfilename = 'Process_' + os.path.basename(filename)

    # Open the output file for writing
    with open(outfilename, 'w') as outfile:
        # Write the processed lines to the output file
        for line in lines:
            outfile.write(line + '\n')

    print(f"Processed data written to {outfilename}.")

if __name__ == '__main__':
    # Read the config file
    config = configparser.ConfigParser()
    config.read('configsample.ini')

    # Loop through all the sections in the config file
    for section_name in config.sections():
        process_file(section_name)
