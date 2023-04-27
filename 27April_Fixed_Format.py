import configparser
import os

config = configparser.ConfigParser()
config.read('configsample.ini')

# Create a new directory for the output files
output_dir = '27April_Output'
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

        # Initialize counts and positions
        count_0, count_1 = 0, 0
        positions_0, positions_1 = [], []

        # Iterate through each line and count 0's and 1's and their positions
        for i in range(min(len(lines1), len(lines2))):
            if lines1[i] != lines2[i]:
                for j in range(min(len(lines1[i]), len(lines2[i]))):
                    if lines1[i][j] != lines2[i][j]:
                        if lines1[i][j] == '0':
                            count_0 += 1
                            positions_0.append((i+1, j+1))
                        elif lines1[i][j] == '1':
                            count_1 += 1
                            positions_1.append((i+1, j+1))

        # Sort positions in ascending order
        positions_0 = sorted(positions_0)
        positions_1 = sorted(positions_1)

        # Write output file with counts and positions
        with open(output_file, 'w') as output:
            output.write(f'Total changes:\n')
            for pos in sorted(positions_0 + positions_1):
                if pos in positions_0:
                    output.write(f'{pos}, "0", SetTo "1"\n')
                elif pos in positions_1:
                    output.write(f'{pos}, "1", SetTo "0"\n')


def process_section(section, section_items, output_dir):
    first_file = section_items[0][1]
    for item in section_items[1:]:
        current_file = item[1]
        output_file = os.path.join(output_dir, f"{first_file}_vs_{current_file}.txt")
        process_files(first_file, current_file, output_file)

# Create output folder if it doesn't exist
output_dir = "27April_Output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through each section in the config file
for section in config.sections():
    section_items = list(config.items(section))
    if section in ['on_off', 'temp', 'mode', 'fan', 'vlourve', 'hlourve', 'misc1', 'misc2']:
        process_section(section, section_items, output_dir)