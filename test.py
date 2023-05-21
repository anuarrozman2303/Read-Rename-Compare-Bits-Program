import os
import configparser
import re

def combine_hex_pos_differences(differences):
    hex_pos_dict = {}
    for difference in differences:
        hex_pos = difference[0]
        hex_pos_dict.setdefault(hex_pos, set()).update(difference[1:])
    output = []
    for hex_pos, hex_pos_differences in hex_pos_dict.items():
        if len(hex_pos_differences) == 1:
            diff_str = str(hex_pos_differences.pop())
        else:
            diff_str = ','.join(str(d) for d in sorted(hex_pos_differences))
        output.append(f"{hex_pos} {diff_str}")
    return output

def process_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        # Filter process
        lines = [line.split(':', 1)[-1] for line in lines]
        lines = [''.join([c for c in line if not c.isalpha()]) for line in lines]
        lines = [line.replace(':', '', 1) for line in lines]
        # Remove empty lines & move up the data.
        lines = [line.strip() for line in lines if line.strip()]

        # Sort into groups of 8 consecutive "0" and "1"
        groups = ["".join(lines[i:i+8]) for i in range(0, len(lines), 8)]
        return lines, groups

def compare_files(file1, file2, differences_set):
    content1, group1 = process_file(file1)
    content2, group2 = process_file(file2)
    differences = []
    jsonformat1 = f'{{"name":"{file1}","inst":['
    jsonformat2 = f'{{"name":"{file2}","inst":['
    for i, (line1, line2) in enumerate(zip(content1, content2)):
        if line1 != line2:
            hex_pos = (i // 8) + 1
            if hex_pos in [8, 16, 35]:
                continue
            diff_str = str(i + 1)
    for i in range(0, len(content1), 8):
        group1 = content1[i:i+8]
        group2 = content2[i:i+8]
        if group1 != group2:
            hex_pos = (i // 8) + 1
            if hex_pos in [8, 16, 35]:
                continue
            # Invert 8-bits value
            binary_str1 = ''.join(str(group1)[::-1])
            binary_str2 = ''.join(str(group2)[::-1])
            # Remove other things except 8-bits binary
            input1 = int(binary_str1.replace('[','').replace(']','').replace(',','').replace(' ','').replace("'", ''), 2)
            input2 = int(binary_str2.replace('[','').replace(']','').replace(',','').replace(' ','').replace("'", ''), 2)
            diff_pos = (int(diff_str) % 8)

            cond1 = diff_pos in range(1, 5)
            cond2 = diff_pos in range(5, 9) or diff_pos == 0
            cond3 = cond1 and cond2
            header = '{"id":"' + section + '","cmd":['

            if cond1:
                jsonformat1 += f'[{hex_pos},15,12],[{hex_pos},{input1},12],'
                jsonformat2 += f'[{hex_pos},15,12],[{hex_pos},{input2},12],'
            if cond2:
                jsonformat1 += f'[{hex_pos},240,12],[{hex_pos},{input1},12],'
                jsonformat2 += f'[{hex_pos},240,12],[{hex_pos},{input2},12],'
            if cond3:
                jsonformat1 += f'[{hex_pos},255,12],[{hex_pos},{input1},12],'
                jsonformat2 += f'[{hex_pos},255,12],[{hex_pos},{input2},12],'

    jsonformat1 = jsonformat1.rstrip(',') + ']}'
    jsonformat2 = jsonformat2.rstrip(',') + ']}'

    if jsonformat1 != jsonformat2:
        differences_set.add((jsonformat1, jsonformat2))
    return hex_pos, input1, input2, differences

config = configparser.ConfigParser()
config.read('configsample.ini')

# Create a new directory to hold the comparison results
if not os.path.exists('8Bits'):
    os.makedirs('8Bits')
    
# Open the output file to write all the output
output_file = os.path.join('8Bits', 'output.json')
with open(output_file, 'w') as f:
    max_input2 = float('-inf')
    # Loop through each section in the config file
    for section in config.sections():
        # Create a set to store all the unique differences
        all_differences = set()
        section_results = [(item, filename) for item, filename in config.items(section) if os.path.isfile(filename)]
        if len(section_results) > 1:
            # Compare the files in this section
            hex_pos = None
            first_comparison_processed = False  # Initialize the flag variable
            for i in range(len(section_results)):
                for j in range(i+1, len(section_results)):
                    item1, filename1 = section_results[i]
                    item2, filename2 = section_results[j]
                    # Receive the values of hex_pos_values, input1_values, and input2_values
                    hex_pos, input1_values, input2_values, _ = compare_files(filename1, filename2, all_differences)
                    if section == "temp" and not first_comparison_processed:
                        min_input1 = input1_values # Update the minimum value
                        first_comparison_processed = True  # Set the flag variable
                        hex_pos = hex_pos
                    max_input2 = max(max_input2, input2_values)

        # Get the unique differences 
        unique_differences = combine_hex_pos_differences(all_differences)

        # Check if the section is "temp"
        if section != "temp":
            f.write(''.join(unique_differences))
        else:
            # Retrieve the items in the "temp" section
            temp_items = config.items(section)
            # Extract the filenames from the items
            filenames = [re.sub(r'\D', '', filename) for _, filename in temp_items]
            temp1 = float(filenames[0])
            temp2 = float(filenames[1])
            templ = float(filenames[-1])
            incr = temp2 - temp1
            disp = int(min_input1 / temp1)
            mintemp = min_input1
            maxtemp = max_input2
            f.write('\n"tCod":[' + f"{disp}," + f"{mintemp}," + f"{maxtemp}],\n")
            f.write('"tDis":[' + f"{incr}," + f"{temp1},{templ}],\n")
            f.write('"tAdd":' + f"{hex_pos},\n")
            f.write('"tUnit":' + '"C"\n')
