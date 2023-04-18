import configparser

# Load config.ini
config = configparser.ConfigParser()
config.read('config.ini')

input_file1 = config.get('command files', 'on_format')
input_file2 = config.get('command files', 'off_format')

with open(input_file1, 'r') as f1, open(input_file2, 'r') as f2:
    lines1 = f1.readlines()
    lines2 = f2.readlines()

for i in range(len(lines1)):
    # Split the line by ":"
    lines1[i] = lines1[i].split(':', 1)[-1]
    # Remove any alphabets
    lines1[i] = ''.join([c for c in lines1[i] if not c.isalpha()])
    # Replace the second ":" with an empty string
    lines1[i] = lines1[i].replace(':', '', 1)

for i in range(len(lines2)):
    lines2[i] = lines2[i].split(':', 1)[-1]
    lines2[i] = ''.join([c for c in lines2[i] if not c.isalpha()])
    lines2[i] = lines2[i].replace(':', '', 1)

# Rewrite
with open(input_file1, 'w') as f1, open(input_file2, 'w') as f2:
    f1.writelines(lines1)
    f2.writelines(lines2)

# Comparison
with open(input_file1, 'r') as file1, open(input_file2, 'r') as file2:
    lines1 = file1.readlines()
    lines2 = file2.readlines()

    # Compare the lines in both files and print the differences
    for i in range(min(len(lines1), len(lines2))):
        if lines1[i] != lines2[i]:
            print(f'Line {i + 1} in both files is different:')
