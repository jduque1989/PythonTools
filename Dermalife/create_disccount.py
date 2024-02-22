import csv


def read_csv_as_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        # Convert the rows to a list format without any modifications
        data_list = [row for row in reader]
    return data_list


text_data_list = read_csv_as_text("./resultado_sku.csv")
# Extracting each line from '{' to '}' while preserving the exact format
formatted_extracted_lines = []
for row in text_data_list:
    joined_row = "".join(row)  # Joining all columns
    if "{" in joined_row and "}" in joined_row:
        start_index = joined_row.find("{")
        end_index = joined_row.find("}") + 1  # +1 to include the closing brace
        formatted_extracted_lines.append(joined_row[start_index:end_index])

print(formatted_extracted_lines)
