import os
import configparser

def process_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        # Filter process
        for i in range(len(lines)):
            lines[i] = lines[i].split(':', 1)[-1]
            lines[i] = ''.join([c for c in lines[i] if not c.isalpha()])
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
            hex_pos_dict[hex_pos] = []
        hex_pos_dict[hex_pos].extend(difference[1:])
    output = []
    for hex_pos, hex_pos_differences in hex_pos_dict.items():
        combined_differences = ','.join(hex_pos_differences)
        output.append(f"[{hex_pos}: {combined_differences}]")
    return '\n'.join(output)

def compare_files(file1, file2):
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
    if not differences:
        return "Files are identical"
    else:
        combined_differences = combine_hex_pos_differences(differences)
        return combined_differences


config = configparser.ConfigParser()
config.read('configsample.ini')

# Create a new directory to hold the comparison results
if not os.path.exists('comparison_results'):
    os.makedirs('comparison_results')

for section in config.sections():
    section_results = []
    section_comparisons = []
    for item, filename in config.items(section):
        if not os.path.isfile(filename):
            continue
        section_results.append((item, filename))
    if len(section_results) > 1:
        # Compare the files in this section
        section_dir = os.path.join('comparison_results', section)
        if not os.path.exists(section_dir):
            os.makedirs(section_dir)
        for i in range(len(section_results)):
            for j in range(i+1, len(section_results)):
                item1, filename1 = section_results[i]
                item2, filename2 = section_results[j]
                differences = compare_files(filename1, filename2)
                if differences == "Files are identical":
                    result = f"{item1} & {item2} are identical."
                else:
                    result = f"{item1} & {item2}: {differences}"
                section_comparisons.append(result)
        # Write the section-specific comparison results to a text file
        result_file = os.path.join(section_dir, f"{section}_comparison.txt")
        with open(result_file, 'w') as f:
            f.write('\n'.join(section_comparisons))
