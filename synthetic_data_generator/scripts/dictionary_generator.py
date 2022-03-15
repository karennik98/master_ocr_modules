import argparse
import random


def get_letters(letters_file):
    return open(letters_file, 'r').readline().split('_')


def generate_words(letters, count, min_size, max_size):
    range = list()
    words = list()
    while min_size <= max_size:
        range.append(min_size)
        min_size += 1
    while count != 0:
        word_length = random.choice(range)
        word_list = random.sample(letters, word_length)
        words.append(''.join(word_list))
        count -= 1
    return words


def write_dict(words, output_file):
    dict = open(output_file, "w")
    for word in words:
        dict.write(word + '\n')
    dict.close()


def main(letters_file, output_file, count, min_size, max_size):
    letters = get_letters(letters_file)
    words = generate_words(letters, count, min_size, max_size)
    write_dict(words, output_file)
    return letters


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate dictionary file"
    )

    parser.add_argument(
        "--big_letters_file",
        type=str,
        nargs="?",
        help="The big letters file",
        default=""
    )

    parser.add_argument(
        "--small_letters_file",
        type=str,
        nargs="?",
        help="The small letters file",
        default=""
    )

    parser.add_argument(
        "--numbers_file",
        type=str,
        nargs="?",
        help="The numbers file",
        default=".txt"
    )

    parser.add_argument(
        "--output_file",
        type=str,
        nargs="?",
        help="The output dictionary file",
        default="dict.txt"
    )

    parser.add_argument(
        "--words_count",
        type=int,
        nargs="?",
        help="The count of generated words",
        default=100
    )

    parser.add_argument(
        "--min_size",
        type=int,
        nargs="?",
        help="The min size for words",
        default=2
    )

    parser.add_argument(
        "--max_size",
        type=int,
        nargs="?",
        help="The max size for words",
        default=10
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    main(args.letters_file, args.output_file, args.words_count, args.min_size, args.max_size)
