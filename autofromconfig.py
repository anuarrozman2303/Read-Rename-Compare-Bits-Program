import configparser
import filecmp

config = configparser.ConfigParser()
config.read('config.ini')

for section in config.sections():
    section_items = list(config.items(section))
    num_items = len(section_items)
    
    for i in range(0, num_items - 1, 2):
        file1 = section_items[i][1]
        file2 = section_items[i+1][1]
        are_files_equal = filecmp.cmp(file1, file2)
        
        if are_files_equal:
            print(f"Files {file1} and {file2} in section '{section}' are equal")
        else:
            print(f"Files {file1} and {file2} in section '{section}' are not equal")
