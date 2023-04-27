import os
import configparser

# Create the output directory if it doesn't exist
output_dir = "Output25April"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

config = configparser.ConfigParser()
config.read('config.ini')

# Loop through each section in the config file
for section in config.sections():
    if section in ['on_off', 'temp', 'mode', 'fanspeed', 'vlourve', 'hlourve', 'special', 'comfort']:
        section_items = list(config.items(section))
        output_path = os.path.join(output_dir, f"{section}.txt")
        # Open the output file for writing
        with open(output_path, 'w') as output:
            output.write(f"--- {section} ---\n")
            first_file = section_items[0][1]
            for item in section_items[1:]:
                current_file = item[1]
                framebr_count = 0
                keys = [section_items[0][0], item[0]]
                output.write(f"Comparing {keys[0]} with {keys[1]}\n")
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
                    output_lines = []
                    # Print the comparison results horizontally
                    for i in range(min(len(lines1), len(lines2))):
                        output_lines.append(f'{lines1[i].strip():<40}{lines2[i].strip()}')
                        if (i+1) % 64 == 0 and framebr_count <= 1:
                            output_lines.append('Frame Break')
                            framebr_count += 1
                    output.write('\n'.join(output_lines) + '\n\n')

                    ## File errors warning.
                    ## Can remove if unnecessary.
                    if len(lines1) != len(lines2):
                        output.write('Warning: Files have different number of lines\n\n')
                    if len(lines1) == 0:
                        output.write('Error: File 1 is empty\n\n')
                    if len(lines2) == 0:
                        output.write('Error: File 2 is empty\n\n')
                    if len(lines1) != len(lines2):
                        output.write('Warning: Files have different number of lines\n\n')
