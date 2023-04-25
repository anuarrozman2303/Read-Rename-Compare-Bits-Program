import os
import configparser

# Create a new directory called "OutputTest3" if it doesn't exist
if not os.path.exists('OutputTest3'):
    os.makedirs('OutputTest3')

config = configparser.ConfigParser()
config.read('config.ini')

# Loop through each section in the config file
for section in config.sections():
    section_items = list(config.items(section))
    if section in ['on_off', 'temp', 'mode', 'fanspeed', 'vswing', 'hswing', 'special', 'comfort']:
        # Create a new output file for this section in the "OutputTest3" directory
        filename = os.path.join('OutputTest3', f"{section}.txt")
        with open(filename, 'w') as output:
            section_items = list(config.items(section))
            output.write(f"--- {section} ---\n")
            first_file = section_items[0][1]
            frame_break_count = [0, 0]  # counter variable for "Frame Break"
            for item in section_items[1:]:
                current_file = item[1]
                keys = [section_items[0][0], item[0]]
                output.write(f"Comparing {keys[0]} with {keys[1]}\n")
                with open(first_file, 'r') as f1, open(current_file, 'r') as f2:
                    lines1 = f1.readlines()
                    lines2 = f2.readlines()
                    # Filter process for file1
                    for i in range(len(lines1)):
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
                        if i % 64 == 63:
                            if frame_break_count[i // 64] < 2:  # print "Frame Break" twice
                                output_lines.append('Frame Break')
                                frame_break_count[i // 64] += 1
                            else:
                                frame_break_count[i // 64] = 0  # reset counter after second "Frame Break"
                    output.write('\n'.join(output_lines) + '\n\n')

                    # File errors warning.
                    # Can remove if unnecessary.
                    if len(lines1) != len(lines2):
                            output.write('Warning: Files have different number of lines\n\n')
