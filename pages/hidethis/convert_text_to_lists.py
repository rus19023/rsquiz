def read_file_in_groups(file_path, group_size=5):
    grouped_lines = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i in range(0, len(lines), group_size):
        group = lines[i:i + group_size]
        grouped_lines.append([line.strip() for line in group])

    return grouped_lines


def write_groups_to_grouped(groups, grouped_path):
    with open(grouped_path, 'w') as grouped:
        grouped.write("grouped_lines = [\n")
        for group in groups:
            grouped.write(f"    {group},\n")
        grouped.write("]\n")


# Convert text to json
file_path = 'quiztest.txt'
file_path = .txt'
grouped_lines = read_file_in_groups(file_path)

# for group in grouped_lines:
#     print(group)
file_path = 'quiz.txt'
grouped_path = 'converted.py'

grouped_lines = read_file_in_groups(file_path)
write_groups_to_grouped(grouped_lines, grouped_path)

print(f"Grouped lines have been written to {grouped_path}")

