import os
import re


def get_current_location():
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_absolute_path(filename: str):
    if filename.startswith('/'):
        # print("root -> ", filename)
        return filename
    elif filename.startswith('~/'):
        # print("home -> ", filename)
        return filename
    elif filename.startswith('../'):
        # print("../ -> ", filename)
        return os.path.join(get_current_location(), filename)
    else:
        # print("relative ->  ", filename)
        return os.path.join(get_current_location(), "../", filename)


def replace_text_in_file(file_path, start_tag, end_tag, output_string):

    if file_path is None:
        print("No `file_path` has been provided, therefore nothing can be stored")
        return

    if start_tag is None or end_tag is None:
        start_tag = ""
        end_tag = ""
        print("start_tag and end_tag have not been provided. Therefore the entire file content will be replaced")

    output_string = start_tag + '\n' + output_string + end_tag

    # Read in the file
    with open(file_path, 'r') as file:
        filedata = file.read()

    # print(f"filedata {filedata}")

    pattern = re.escape(start_tag) + ".*" + re.escape(end_tag)
    replaced = re.sub(pattern, output_string, filedata, flags=re.DOTALL)

    # print(f"replaced {replaced}")

    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(replaced)

    return replaced


def print_to_file(output_file_path, content: list):
    file = open(output_file_path, "w")
    for line in content:
        file.write(line + "\n")
    file.close()
