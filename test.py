import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

def process_files(file1, file2):
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
        with open(file1, 'w') as f1, open(file2, 'w') as f2:
            f1.writelines('\n'.join(lines1))
            f2.writelines('\n'.join(lines2))
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
            for i in range(min(len(lines1), len(lines2))):
                if lines1[i] != lines2[i]:
                    print("---------------------------")
                    print(f'Line {i + 1}:')
                    print(f'{file1}: {lines1[i]}')
                    print(f'{file2}: {lines2[i]}')

# Loop through each section in the config file
for section in config.sections():
    section_items = list(config.items(section))
    num_items = len(section_items)
    if section == 'on_off':
        print("---------------------------")
        print(f"Processing section: {section}")
        for i in range(0, num_items - 1, 2):
            file1 = section_items[i][1]
            file2 = section_items[i+1][1]
            process_files(file1, file2)
    if section == 'temp':
        print("---------------------------")
        print(f"Processing section: {section}")
        for i in range(0, num_items - 1, 2):
            file1 = section_items[i][1]
            file2 = section_items[i+1][1]
            process_files(file1, file2)

