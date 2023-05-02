import configparser
import os

config = configparser.ConfigParser()
config.read('configsample.ini')

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
                    output.write(f'{section}\n')
                    output.write(f'Line {i + 1}:\n')
                    output.write(f'{file1}: {lines1[i]}\n')
                    output.write(f'{file2}: {lines2[i]}\n')

def process_section(section, section_items):
    section_dir = os.path.join("Bits_Pos", section)
    os.makedirs(section_dir, exist_ok=True)
    for i, item in enumerate(section_items):
        if i == len(section_items) - 1:
            break
        file1 = item[1]
        for j in range(i + 1, len(section_items)):
            file2 = section_items[j][1]
            output_file = os.path.join(section_dir, f"{os.path.splitext(os.path.basename(file1))[0]}_vs_{os.path.splitext(os.path.basename(file2))[0]}.txt")
            if os.path.exists(file1) and os.path.exists(file2):
                process_files(file1, file2, output_file)

# Loop through each section in the config file
for section in config.sections():
    section_items = list(config.items(section))
    if section in ['on_off', 'temp', 'mode', 'fan', 'vlourve', 'hlourve', 'misc1', 'misc2']:
        process_section(section, section_items)
