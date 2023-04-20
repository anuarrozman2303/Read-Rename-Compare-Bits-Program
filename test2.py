filename = "on.txt"
line_count = 0

# Open the file for reading
with open(filename, "r") as file:
    # Loop through each line in the file
    for line in file:
        # Increment the line count
        line_count += 1

        # Check if a break point has been reached
        if line_count == 64 or line_count == 128:
            print("Break point reached at line", line_count)

# Print the total line count
print("Total number of lines:", line_count)