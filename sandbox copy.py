import re

# Step 1: Extract parts of the lines after the hyphen
text = """[0:0.00] - jos We equally reject attempts to prescribe new rights that are contrary to our values,
[0:9.28] - norms, that aint it traditions and beliefs. We are not gays.
[0:16.00] - Cooperation and respect for each other will advance the cause of human rights worldwide.
[0:25.00] - Confrontation, vilification and double standards will not.
[0:31.00] - Mr. President, self-determination and independence are intrinsic and fundamental rights
[0:39.00] - that should be enjoyed by all people everywhere without distinction.
[0:45.00] - We are deeply concerned by the continued denial of this basic right to the Sahara-Saharawi people.
[0:54.00] - United Nations to expeditiously finalize what must be done to conclude the decolonization of the Western Sahara."""

# Extracting the text after the hyphen
lines = text.split('\n')
extracted_text = [line.split(' - ', 1)[1] if ' - ' in line else '' for line in lines]

# Step 2: Open and read the .ass file
ass_file_path = 'sub-Mugabe1.en.ass'  # replace with your file path

with open(ass_file_path, 'r') as file:
    ass_file_content = file.read()

# Split the .ass file content into lines
ass_lines = ass_file_content.split('\n')

# Step 3: Replace dialogue lines
new_ass_lines = []
extracted_index = 0

for line in ass_lines:
    if line.startswith('Dialogue:') and extracted_index < len(extracted_text):
        parts = line.split(',', 9)
        if len(parts) == 10:
            parts[9] = extracted_text[extracted_index]
            extracted_index += 1
        new_ass_lines.append(','.join(parts))
    else:
        new_ass_lines.append(line)

new_ass_content = '\n'.join(new_ass_lines)

# Step 4: Write the updated content back to the .ass file
with open(ass_file_path, 'w') as file:
    file.write(new_ass_content)

# Optional: Print the updated .ass content to verify
print(new_ass_content)
