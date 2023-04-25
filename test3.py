import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Create the output directory if it doesn't exist
if not os.path.exists('Output25April'):
    os.makedirs('Output25April')

# Loop through each section in the config file
for section in config.sections():
    if section in ['on_off', 'temp', 'mode', 'fanspeed', 'vswing', 'hswing', 'special', 'comfort']:
        section_items = list(config.items(section))
        output_path = f'Output25April/{section}.txt'
        # Open the output file for writing
        with open(output_path, 'w') as output:
            output_lines = []
            output_lines.append(f'--- {section} ---\n\n')
            first_file = section_items[0][1]
            for item in section_items[1:]:
                current_file = item[1]
                keys = [section_items[0][0], item[0]]
                output_lines.append(f'Comparing {keys[0]} with {keys[1]}:\n\n')
                with open(first_file, 'r') as f1, open(current_file, 'r') as f2:
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
                    # Print the comparison results horizontally
                    for i in range(min(len(lines1), len(lines2))):
                        if i == 56 or i == 120 or i == 271:
                            output_lines.append('ChSum'.ljust(40) + '|' + f'{i+1:02d}'.rjust(3) + '|' + lines1[i].strip().ljust(28) + '|' + lines2[i].strip())
                        else:
                            output_lines.append(lines1[i].strip().ljust(40) + '|' + f'{i+1:02d}'.rjust(3) + '|' + lines2[i].strip())
                    # Add warning messages for file errors
                    if len(lines1) != len(lines2):
                        output_lines.append('\nWarning: Files have different number of lines')
                    if len(lines1) == 0:
                        output_lines.append('\nError: File 1 is empty')
                    if len(lines2) == 0:
                        output_lines.append('\nError: File 2 is empty')
                    output_lines.append('\n\n')
            # Write all output lines to the file
            output.writelines(output_lines)
