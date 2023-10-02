import sys
import csv

if len(sys.argv) < 2:
    print("Please provide the input file path as the first argument.")
    sys.exit()

input_file = sys.argv[1]
output_file = "names.txt"

with open(input_file, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    formatted_data = []
    for row in csv_reader:
        name = row[0]
        details = row[1:]
        # Format the name (remove the prefix)
        formatted_name = name.split(' ', 1)[-1]
        # Append the formatted entry to the output list
        formatted_data.append([formatted_name] + details)

with open(output_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(formatted_data)

print(f"Formatted data has been written to {output_file}")
