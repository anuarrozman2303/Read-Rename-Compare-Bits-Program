import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

def process_files(on_file, off_file):
    with open(on_file, 'r') as f1, open(off_file, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        # Filter process for file1
        for i in range(len(lines1)):
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
        with open(on_file, 'w') as f1, open(off_file, 'w') as f2:
            f1.writelines('\n'.join(lines1))
            f2.writelines('\n'.join(lines2))
        with open(on_file, 'r') as file1, open(off_file, 'r') as file2:
            lines1 = file1.readlines()
            lines2 = file2.readlines()
            for i in range(min(len(lines1), len(lines2))):
                if lines1[i] != lines2[i]:
                    print("---------------------------")
                    print(f'Line {i + 1}:')
                    print(f'{on_file}: {lines1[i]}')
                    print(f'{off_file}: {lines2[i]}')
def process_files(temp1_file, temp2_file):
    with open(temp1_file, 'r') as f1, open(temp2_file, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        # Filter process for file1
        for i in range(len(lines1)):
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
        with open(on_file, 'w') as f1, open(off_file, 'w') as f2:
            f1.writelines('\n'.join(lines1))
            f2.writelines('\n'.join(lines2))
        with open(temp1_file, 'r') as file1, open(temp2_file, 'r') as file2:
            lines1 = file1.readlines()
            lines2 = file2.readlines()
            for i in range(min(len(lines1), len(lines2))):
                if lines1[i] != lines2[i]:
                    print("---------------------------")
                    print(f'Line {i + 1}:')
                    print(f'{temp1_file}: {lines1[i]}')
                    print(f'{temp2_file}: {lines2[i]}')

# Loop through each section in the config file
for section_name in config.sections():
    print("---------------------------")
    print(f"Processing section: {section_name}")
    section = config[section_name]

    # Check the section name and perform different actions for each section
    if section_name == 'on_off':
        on_file = section.get('on_format', section_name)
        off_file = section.get('off_format', section_name)
        process_files(on_file, off_file)
    elif section_name == 'temp':
        temp1_file = section.get('temp25_format', section_name)
        temp2_file = section.get('temp26_format', section_name)
        process_files(temp1_file, temp2_file)
    elif section_name == 'mode':
        cold_file = section.get('mode_cold_format', '')
        dry_file = section.get('mode_dry_format', '')
        if os.path.isfile(cold_file):
            with open(cold_file, 'r') as f:
                file_contents = f.read()
            print(f"Cold mode file '{cold_file}' contains:\n{file_contents}")
        else:
            print(f"Cold mode file '{cold_file}' not found.")
        if os.path.isfile(dry_file):
            with open(dry_file, 'r') as f:
                file_contents = f.read()
            print(f"Dry mode file '{dry_file}' contains:\n{file_contents}")
        else:
            print(f"Dry mode file '{dry_file}' not found.")
    else:
        print(f"Unknown section '{section_name}'")
