import json

# Import the lists from the Python file
from grouped_lines import grouped_lines

# Define the path to the JSON file
json_file_path = 'quiz.json'

# Write the lists to a JSON file
with open(json_file_path, 'a') as json_file:
    json.dump(grouped_lines, json_file, indent=4)

print(f"Grouped lines have been written to {json_file_path}")
