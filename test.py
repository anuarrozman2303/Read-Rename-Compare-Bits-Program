# Open the file in binary mode for reading
with open('C:\\Python\\IR Compare\\Daikin\\Commands\\default.txt', 'rb') as file:
    contents = file.read()
    # Convert to a string
    contents_str = contents.decode('utf-8')
    # Filter out all characters that are not '0' or '1'
    filtered_str = ''.join(c for c in contents_str if c in ('0', '1'))
    # Print the filtered string
    print(filtered_str)