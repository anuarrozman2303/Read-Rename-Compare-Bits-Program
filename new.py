## This code will process the export files from PulseView.
## The process files will be sort based on sections in the config file.
## Then the files for key-value in section will be compared.
## The difference data locations will be printed out as [<hex_pos>: <bit_positions>]
## The unique <bit_positions> in each sections will be printed out in the terminal.
## <section_name>
## [<hex_pos>: <list_of_unique_bit_position>]

import os
import configparser

def process_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        # Filter process
        for i in range(len(lines)):
            lines[i] = lines[i].split(':', 1)[-1]
            lines[i] = ''.join([c for c in lines[i] if not c.isalpha( )])
            lines[i] = lines[i].replace(':', '', 1)
        # Remove empty lines & move up the data.
        lines = [line.strip() for line in lines if line.strip()]
        return lines

def group_by_hex_pos(differences):
    hex_pos_dict = {}
    for difference in differences:
        hex_pos = difference[0]
        if hex_pos not in hex_pos_dict:
            hex_pos_dict[hex_pos] = []
        hex_pos_dict[hex_pos].append(difference[1:])
    return hex_pos_dict

def combine_hex_pos_differences(differences):
    hex_pos_dict = {}
    for difference in differences:
        hex_pos = difference[0]
        if hex_pos not in hex_pos_dict:
            hex_pos_dict[hex_pos] = set()
        hex_pos_dict[hex_pos].update(difference[1:])
    output = []
    for hex_pos, hex_pos_differences in hex_pos_dict.items():
        if len(hex_pos_differences) == 1:
            diff_str = str(hex_pos_differences.pop())
        else:
            diff_str = ','.join(str(d) for d in sorted(hex_pos_differences))
        output.append(f"[{hex_pos}: {diff_str}]")
    return output

def compare_files(file1, file2, differences_set):
    content1 = process_file(file1)
    content2 = process_file(file2)
    differences = []
    for i, (line1, line2) in enumerate(zip(content1, content2)):
        if line1 != line2:
            hex_pos = (i // 8) + 1
            if hex_pos in [8, 16, 35]:
                continue
            diff_str = str(i+1)
            differences.append((hex_pos, diff_str))
    if differences:
        differences_set.update(differences)
        print(f"Differences between {file1} and {file2}:")
        for difference in differences:
            print(f"  Hex position: {difference[0]}, Bit position: {difference[1]}")


config = configparser.ConfigParser()
config.read('configsample.ini')

# Create a new directory to hold the comparison results
if not os.path.exists('Unique_BitPos'):
    os.makedirs('Unique_BitPos')

# Loop through each section in the config file
for section in config.sections():
    # Create a set to store all the unique differences
    all_differences = set()
    section_results = []
    section_comparisons = []
    for item, filename in config.items(section):
        if not os.path.isfile(filename):
            continue
        section_results.append((item, filename))
    if len(section_results) > 1:
        # Compare the files in this section
        for i in range(len(section_results)):
            for j in range(i+1, len(section_results)):
                item1, filename1 = section_results[i]
                item2, filename2 = section_results[j]
                compare_files(filename1, filename2, all_differences)

    # Get the unique differences
    unique_differences = combine_hex_pos_differences(all_differences)

    # Write the output to a text file
    output_file = os.path.join('Unique_BitPos', f"{section}.txt")
    with open(output_file, 'w') as f:
        f.write('\n'.join(unique_differences))




