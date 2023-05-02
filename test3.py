import configparser
import os

config = configparser.ConfigParser()
config.read('configsample.ini')

# Create a new directory for the output files
output_dir = "Output"
os.makedirs(output_dir, exist_ok=True)

def process_files(file1, file2, output_file, section):
    # Create the Output folder if it doesn't exist
    if not os.path.exists('Output'):
        os.makedirs('Output')
        
    # Create the section folder if it doesn't exist
    section_folder = os.path.join('Output', section)
    if not os.path.exists(section_folder):
        os.makedirs(section_folder)
    
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
        with open(output_file, 'a') as output:
            for i in range(min(len(lines1), len(lines2))):
                if lines1[i] != lines2[i]:
                    output.write("---------------------------\n")
                    output.write(f'{section}\n')
                    output.write(f'Line {i + 1}:\n')
                    output.write(f'{file1}: {lines1[i]}\n')
                    output.write(f'{file2}: {lines2[i]}\n')


def process_section(section, section_items, output_dir):
    # create a list to store the output for this section
    section_output = []

    # iterate over each item in the section
    for i, item in enumerate(section_items):
        # get the filename and check if it exists
        filename = item[1]
        if not os.path.exists(filename):
            print(f"WARNING: File '{filename}' not found for section '{section}'. Skipping...")
            continue

        # compare this file with the next file (if there is one)
        if i < len(section_items) - 1:
            next_filename = section_items[i+1][1]
            if not os.path.exists(next_filename):
                print(f"WARNING: File '{next_filename}' not found for section '{section}'. Skipping...")
                continue
            output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(filename))[0]}_vs_{os.path.splitext(os.path.basename(next_filename))[0]}.txt")
            process_files(filename, next_filename, output_file, section)
            section_output.append(output_file)

    # combine the section output into a single file
    if section_output:
        combined_output_file = os.path.join(output_dir, f"{section}.txt")
        with open(combined_output_file, "w") as f:
            for output_file in section_output:
                with open(output_file, "r") as f_input:
                    f.write(f_input.read())
        print(f"Combined output for section '{section}' written to '{combined_output_file}'")
    else:
        print(f"No output files generated for section '{section}'")



# Create output folder if it doesn't exist
output_dir = "Output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through each section in the config file
for section in config.sections():
    section_items = list(config.items(section))
    if section in ['on_off', 'temp', 'mode', 'fan', 'vlourve', 'hlourve', 'misc1', 'misc2']:
        process_section(section, section_items, output_dir)
