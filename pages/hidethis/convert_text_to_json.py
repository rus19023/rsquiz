import json

def read_and_process_file(file_path, group_size=5):
    def line_generator():
        with open(file_path, 'r') as file:
            for line in file:
                yield line.strip()

    gen = line_generator()
    while True:
        group = [next(gen, None) for _ in range(group_size)]
        if group[0] is None:
            break
        yield [line for line in group if line is not None]

def write_groups_to_json(input_file, output_file, group_size=5):
    groups = list(read_and_process_file(input_file, group_size))
    
    # Write directly to JSON file without the "grouped_lines" wrapper
    with open(output_file, 'w') as out:
        json.dump(groups, out, indent=2)

# Usage
root = 'pages/hidethis/'
input_file = f'{root}hum110.txt'
output_file = f'{root}questions.json'
write_groups_to_json(input_file, output_file)

print(f"Grouped lines have been written to {output_file} in JSON format")