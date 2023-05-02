import configparser
import os

config = configparser.ConfigParser()
config.read('configsample.ini')

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

        # Write output as string
        # Write output as string
        output_str = f''
        for pos in sorted(hex_positions_0 + hex_positions_1, key=lambda x: x[2]):
            if (((pos[0]-1)//8 + 1) != 8) and (((pos[0]-1)//8 + 1) != 16) and (((pos[0]-1)//8 + 1) != 35):
                if pos in hex_positions_0:
                    output_str += f'["{(pos[0]-1)//8 + 1}","{pos[0]-1}",SetTo 0], ["{(pos[0]-1)//8 + 1}","{pos[0]-1}",SetTo {lines2[pos[0]-1][pos[1]-1]}]\n'
                elif pos in hex_positions_1:
                    output_str += f'["{(pos[0]-1)//8 + 1}","{pos[0]-1}",SetTo 0], ["{(pos[0]-1)//8 + 1}","{pos[0]-1}",SetTo {lines2[pos[0]-1][pos[1]-1]}]\n'
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
        output_file = f'2May_Output{section}.txt'
        with open(output_file, 'w') as f:
            f.write(section_output_str)
