import os
import configparser

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
        output_str = ''.join(lines)
        output_str = '\n'.join([output_str[i:i+8] for i in range(0, len(output_str), 8)])
        return output_str


config = configparser.ConfigParser()
config.read('configsample.ini')

# Create a new directory to hold the processed files
if not os.path.exists('processed_files'):
    os.makedirs('processed_files')

for section in config.sections():
    for item, filename in config.items(section):
        if not os.path.isfile(filename):
            continue
        output_str = process_file(filename)
        print(f"Length of {filename}: {len(output_str)}")  # Check file length
        print(f"Number of 8-character chunks in {filename}: {len(output_str)//8}") # Count 8-character chunks
        output_filename = f'Processed_{os.path.splitext(os.path.basename(filename))[0]}.txt'
        output_path = os.path.join('processed_files', output_filename)
        with open(output_path, 'w') as f:
            f.write(output_str)

 
## Continue Here
## Done Process Files to 1 & 0 into horizontal lists
## --- Read processed files to do comparison.
