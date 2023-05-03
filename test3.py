import configparser
import os

config = configparser.ConfigParser()
config.read('configsample.ini')

def process_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        # Filter process for file1
        lines1 = [line.split(':', 1)[-1] for line in lines1]
        lines1 = [''.join(c for c in line if c in ['0', '1']) for line in lines1]
        lines1 = [line.strip() for line in lines1 if line.strip()]
        # Filter process for file2
        lines2 = [line.split(':', 1)[-1] for line in lines2]
        lines2 = [''.join(c for c in line if c in ['0', '1']) for line in lines2]
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

        # Calculate hex values for positions
        hex_positions_0 = [(pos[0], pos[1], pos[0]*8 + pos[1] - 1) for pos in positions_0]
        hex_positions_1 = [(pos[0], pos[1], pos[0]*8 + pos[1] - 1) for pos in positions_1]

        # Create a dictionary to group the positions by {(pos[0]-1)//8 + 1}
        pos_dict = {}
        for pos in sorted(hex_positions_0 + hex_positions_1, key=lambda x: x[2]):
            group = (pos[0]-1)//8 + 1
            if group not in pos_dict:
                pos_dict[group] = []
            pos_dict[group].append(pos)

        # Write output as string
        output_str = ''
        for group, positions in pos_dict.items():
            output_str += f'[{group}, '
            for pos in positions:
                output_str += f'"{pos[0]}", SetTo 0, ["{pos[0]}","{pos[1]}",SetTo {lines2[pos[0]-1][pos[1]-1]}], '
            output_str = output_str[:-2] + ']\n'

        return output_str

# Loop through each section in the config file
for section in config.sections():
    if section in ['on_off', 'temp', 'mode', 'fan', 'vlourve', 'hlourve', 'misc1', 'misc2']:
        section_output_str = ''
        section_items = list(config.items(section))
        for i, (item1, file1) in enumerate(section_items):
            for item2, file2 in section_items[i+1:]:
                if not os.path.isfile(file1) or not os.path.isfile(file2):
                    continue
                output_str = process_files(file1, file2)
                section_output_str += f'{item1} vs {item2}:\n{output_str}\n'
        # Write output to file
        output_file = f'test3_Output{section}.txt'
        with open(output_file, 'w') as f:
            f.write(section_output_str)
