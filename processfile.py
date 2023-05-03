import configparser
import os

def process_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        # Filter process
        for i in range(len(lines)):
            lines[i] = lines[i].split(':', 1)[-1]
            lines[i] = ''.join([c for c in lines[i] if not c.isalpha()])
            lines[i] = lines[i].replace(':', '', 1)
        # Remove empty lines & move up the data.
        lines = [line.strip() for line in lines if line.strip()]
        return ''.join(lines)

config = configparser.ConfigParser()
config.read('configsample.ini')

for section in config.sections():
    for item, filename in config.items(section):
        if not os.path.isfile(filename):
            continue
        output_str = process_file(filename)
        print
        print(len(process_file(filename)))  # Check file length, = 280 
        output_filename = f'Processed_{os.path.splitext(filename)[0]}.txt'
        with open(output_filename, 'w') as f:
            f.write(output_str)

## Continue Here
## Done Process Files to 1 & 0 into horizontal lists
## --- Read processed files to do comparison.
