import re

def extract_caption_segments(file_path):
    """
    Extracts time and text segments from the given .ass file and formats them.
    
    :param file_path: Path to the .ass file.
    :return: List of tuples with formatted time and text.
    """
    def format_time(time_str):
        """
        Formats time from 'h:mm:ss.cs' to 'm:ss'.
        """
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1]) + hours * 60
        seconds = float(parts[2])
        return f'{minutes:.0f}:{seconds:.2f}'

    output = []
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("Dialogue:"):
                match = re.match(r"Dialogue: \d,(\d+:\d+:\d+\.\d+),\d+:\d+:\d+\.\d+,Default,,\d,\d,\d,,(.*)", line)
                if match:
                    start_time = format_time(match.group(1))
                    text = match.group(2).replace('\\N', ' ')  # Replace newlines in .ass with spaces
                    output.append((start_time, text))
                    
    print(output)
    return output

def update_ass_file(original_file, output_list, result_file):
    """
    Updates the text sections in the .ass file based on the output list from extract_caption_segments.
    
    :param original_file: Path to the original .ass file.
    :param output_list: List of tuples with formatted time and text.
    :param result_file: Path to the result .ass file.
    """
    with open(original_file, 'r') as file:
        lines = file.readlines()

    event_section_started = False
    dialogue_index = 0

    for i, line in enumerate(lines):
        if line.startswith("[Events]"):
            event_section_started = True

        if event_section_started and line.startswith("Dialogue:"):
            if dialogue_index < len(output_list):
                time_text_pair = output_list[dialogue_index]
                match = re.match(r"(Dialogue: \d,\d+:\d+:\d+\.\d+),\d+:\d+:\d+\.\d+,Default,,\d,\d,\d,,(.*)", line)
                if match:
                    start_part = match.group(1)
                    new_text = time_text_pair[1]
                    lines[i] = f"{start_part},{new_text}\n"
                dialogue_index += 1

    with open(result_file, 'w') as file:
        file.writelines(lines)

# Usage
file_path = 'sub-Mugabe1.en.ass'
output_list = extract_caption_segments(file_path)
update_ass_file(file_path, output_list, 'result.ass')

print("The .ass file has been updated successfully!")
