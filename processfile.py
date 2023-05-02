import os

def process_file(filename):
    # Open the input file for reading
    with open(filename, 'r') as infile:
        # Read in all the lines of the file
        lines = infile.readlines()

    # Remove everything before the colon, remove all non-numeric characters, and remove empty lines
    lines = [line.split(':', 1)[-1] for line in lines]
    lines = [''.join(c for c in line if c in ['0', '1']) for line in lines]
    lines = [line.strip() for line in lines if line.strip()]

    ## not working
    # Replace lines 104-111, 168-175, and 176-183 with "0" if filename is "mode_default.txt"
    if os.path.basename(filename) == "mode_default.txt":
        lines[103:111] = ["0"] * 8
        lines[167:175] = ["0"] * 8
        lines[175:183] = ["0"] * 8

    # Replace lines 168-175 with "0" if filename is "default.txt"
    elif os.path.basename(filename) == "default.txt":
        lines[167:175] = ["0"] * 8

    # Replace lines 176-183 with "0" if filename is "temp_default.txt"
    elif os.path.basename(filename) == "temp_default.txt":
        lines[175:183] = ["0"] * 8

    # Create the output filename
    outfilename = 'Process_' + os.path.basename(filename)

    # Open the output file for writing
    with open(outfilename, 'w') as outfile:
        # Write the processed lines to the output file
        for line in lines:
            outfile.write(line + '\n')

    print(f"Processed data written to {outfilename}.")

if __name__ == '__main__':
    filename = input("Enter the name of the file to process: ")
    process_file(filename)
