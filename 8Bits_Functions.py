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

def process_group(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            # Filter process
            for i in range(len(lines)):
                lines[i] = lines[i].split(':', 1)[-1]
                lines[i] = ''.join([c for c in lines[i] if not c.isalpha()])
                lines[i] = lines[i].replace(':', '', 1)
            # Remove empty lines & move up the data.
            lines = [line.strip() for line in lines if line.strip()]

            # Sort into groups of 8 consecutive "0" and "1"
            groups = []
            current_group = ''
            for line in lines:
                current_group += line
                if len(current_group) == 8:
                    groups.append(current_group)
                    current_group = ''
            if current_group:  # In case there's an incomplete group at the end
                groups.append(current_group)

            return groups

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
    group1 = process_group(file1)
    group1 = process_group(file1)
    differences = []
    for i, (line1, line2) in enumerate(zip(content1, content2)):
        if line1 != line2:
            hex_pos = (i // 8) + 1
            if hex_pos in [8, 16, 35]:
                continue
            diff_str = str(i+1) + "\n"
            differences.append((hex_pos, diff_str))
            
    if differences:
        differences_set.update(differences)
    for i in range(0, len(content1), 8):
        group1 = content1[i:i+8]
        group2 = content2[i:i+8]
        if group1 != group2:
            hex_pos = (i // 8) + 1
            if hex_pos in [8, 16, 35]:
                continue
            diff_str1 = ''.join(str(group1)) + f"{file1}\n"
            diff_str2 = ''.join(str(group2)) + f"{file2}\n"
            differences.append((hex_pos, diff_str1))
            differences.append((hex_pos, diff_str2))
    if differences:
        differences_set.update(differences)
        
config = configparser.ConfigParser()
config.read('configsample.ini')

# Create a new directory to hold the comparison results
if not os.path.exists('8Bits'):
    os.makedirs('8Bits')

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
    output_file = os.path.join('8Bits', f"{section}.txt")
    with open(output_file, 'w') as f:
        f.write('\n'.join(unique_differences))




