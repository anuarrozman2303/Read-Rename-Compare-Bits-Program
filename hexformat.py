import re
import configparser

# Read config file
config = configparser.ConfigParser()
config.read('configsample.ini')

# Get input and output filenames from config
default_input_file = config['default']['default']
on_input_file = config['on_off']['on']
off_input_file = config['on_off']['off']
# Repeat for other sections...

# Process default input file
with open(default_input_file, 'r') as f:
    data = f.read()

# Perform processing steps on data
data = re.sub(r'.*?:', '', data, count=2)
data = re.sub(r'[^01]', '', data)
data = data.replace(' ', '').strip()

# Write processed data to output file
default_output_file = 'default_output.txt'
with open(default_output_file, 'w') as f:
    f.write(data)

# Repeat for other sections...
