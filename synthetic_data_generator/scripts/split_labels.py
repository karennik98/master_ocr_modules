import argparse
import re

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Read labels file and create .txt files for all lines"
    )
    parser.add_argument(
        "--labels_file",
        type=str,
        nargs="?",
        help="The labels file",
        default="labels.txt"
    )
    parser.add_argument(
        "--extension",
        type=str,
        nargs="?",
        help="Define the extension of generated labels file",
        default="jpg",
    )
    parser.add_argument(
        "--out_extension",
        type=str,
        nargs="?",
        help="Define the extension of generated files",
        default="txt",
    )
    return parser.parse_args()

def main(labels_path, extension, out_extension):
    file = open(labels_path, "r")
    lines = file.readlines()
    for line in lines:
        pattern = r'.+?.' + extension
        new_file_name = re.search(pattern, line).group()
        if new_file_name:
            new_file_name = new_file_name.replace(extension, out_extension)
            new_file = open(new_file_name, "w")
            line = re.sub(r'.+?.' + extension + ' ', '', line)
            new_file.write(line)
            new_file.close()

if __name__ == "__main__":
    args = parse_arguments()
    main(args.labels_file, args.extension, args.out_extension)