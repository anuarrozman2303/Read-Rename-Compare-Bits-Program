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

def compare_files(file1, file2):
    content1 = process_file(file1)
    content2 = process_file(file2)
    differences = []
    for i, (line1, line2) in enumerate(zip(content1, content2)):
        if line1 != line2:
            differences.append(f"{i+1}: {line1.strip()} != {line2.strip()}")
    if not differences:
        return "Files are identical"
    else:
        return differences


config = configparser.ConfigParser()
config.read('configsample.ini')

# Create a new directory to hold the comparison results
if not os.path.exists('comparison_results'):
    os.makedirs('comparison_results')

for section in config.sections():
    section_results = []
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
                    result = f"{item1} and {item2} are identical."
                else:
                    result = f"{item1} and {item2} differ:\n" + '\n'.join(differences)
                result_file = os.path.join(section_dir, f"{item1}_{item2}_comparison.txt")
                with open(result_file, 'w') as f:
                    f.write(result)


 
## Continue Here
## Done Process Files to 1 & 0 into horizontal lists
## --- Read processed files to do comparison.
