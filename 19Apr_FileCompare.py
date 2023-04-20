import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

# Create a new directory for the output files
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

def process_files(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        # Filter process for file1
        for i in range (len(lines1)):
            lines1[i] = lines1[i].split(':', 1)[-1]
            lines1[i] = ''.join([c for c in lines1[i] if not c.isalpha()])
            lines1[i] = lines1[i].replace(':', '', 1)
        # Filter process for file2
        for i in range(len(lines2)):
            lines2[i] = lines2[i].split(':', 1)[-1]
            lines2[i] = ''.join([c for c in lines2[i] if not c.isalpha()])
            lines2[i] = lines2[i].replace(':', '', 1)
        # Remove empty lines & move up the data.
        lines1 = [line.strip() for line in lines1 if line.strip()]
        lines2 = [line.strip() for line in lines2 if line.strip()]
        with open(output_file, 'w') as output:
            for i in range(min(len(lines1), len(lines2))):
                if lines1[i] != lines2[i]:
                    output.write("---------------------------\n")
                    output.write(f'Line {i + 1}:\n')
                    output.write(f'{file1}: {lines1[i]}\n')
                    output.write(f'{file2}: {lines2[i]}\n')

# Loop through each section in the config file
for section in config.sections():
    section_items = list(config.items(section))
    num_items = len(section_items)
    if section == 'on_off':
        # Extract the file path for the first key-value & save it to first_file
        first_file = section_items[0][1]
        for item in section_items[1:]:
            current_file = item[1]
            output_file = os.path.join(output_dir, f"{first_file}_vs_{current_file}.txt")
            process_files(first_file, current_file, output_file)
    elif section == 'temp':
        # Extract the file path for the first key-value & save it to first_file
        first_file = section_items[0][1]
        for item in section_items[1:]:
            current_file = item[1]
            output_file = os.path.join(output_dir, f"{first_file}_vs_{current_file}.txt")
            process_files(first_file, current_file, output_file)
    elif section == 'mode':
        # Extract the file path for the first key-value & save it to first_file
        first_file = section_items[0][1]
        for item in section_items[1:]:
            current_file = item[1]
            output_file = os.path.join(output_dir, f"{first_file}_vs_{current_file}.txt")
            process_files(first_file, current_file, output_file)
    elif section == 'fanspeed':
        # Extract the file path for the first key-value & save it to first_file
        first_file = section_items[0][1]
        for item in section_items[1:]:
            current_file = item[1]
            output_file = os.path.join(output_dir, f"{first_file}_vs_{current_file}.txt")
            process_files(first_file, current_file, output_file)
    elif section == 'vswing':
        # Extract the file path for the first key-value & save it to first_file
        first_file = section_items[0][1]
        for item in section_items[1:]:
            current_file = item[1]
            output_file = os.path.join(output_dir, f"{first_file}_vs_{current_file}.txt")
            process_files(first_file, current_file, output_file)
    elif section == 'hswing':
        # Extract the file path for the first key-value & save it to first_file
        first_file = section_items[0][1]
        for item in section_items[1:]:
            current_file = item[1]
            output_file = os.path.join(output_dir, f"{first_file}_vs_{current_file}.txt")
            process_files(first_file, current_file, output_file)
    elif section == 'special':
        # Extract the file path for the first key-value & save it to first_file
        first_file = section_items[0][1]
        for item in section_items[1:]:
            current_file = item[1]
            output_file = os.path.join(output_dir, f"{first_file}_vs_{current_file}.txt")
            process_files(first_file, current_file, output_file)
    elif section == 'comfort':
        # Extract the file path for the first key-value & save it to first_file
        first_file = section_items[0][1]
        for item in section_items[1:]:
            current_file = item[1]
            output_file = os.path.join(output_dir, f"{first_file}_vs_{current_file}.txt")
            process_files(first_file, current_file, output_file)


