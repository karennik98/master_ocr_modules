import os
import ctypes

import argparse

lang = "hye"
libname = "/home/karen/installed_libs/tesseract_source/tesseract/build/libtesseract.so"
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/4.00/tessdata'

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Take base dir of data"
    )
    parser.add_argument(
        "--base_dir",
        type=str,
        nargs="?",
        help="The data base dir",
        default="./"
    )

    return parser.parse_args()


def get_sub_dirs(dir):
    subdirs = [f.path for f in os.scandir(dir) if f.is_dir()]
    return subdirs


def get_files_pair(dir):
    all_files = [f.path for f in os.scandir(dir) if f.is_file()]
    files_pair = list()
    for file in all_files:
        if file.find("jpg") !=0:
            dot_pos = file.find(".")
            name = file[0:dot_pos]
            txt_file = name + ".txt"
            files_pair.append((file, txt_file))
    return files_pair


def get_files(base_dir):
    subdirs = get_sub_dirs(base_dir)
    all_files_pair = list()
    for dir_i in subdirs:
        subsubdirs = get_sub_dirs(dir_i)
        for dir_j in subsubdirs:
            files_pair = get_files_pair(dir_j)
            all_files_pair.append(files_pair)
    return all_files_pair

def main(base_dir):
    files = get_files(base_dir)
    for lfiles in files:
        for lfile in lfiles:
            test_tesseract(lfile[0], lfile[1])

def test_tesseract(image, txt):
    TESSDATA_PREFIX = os.environ.get('TESSDATA_PREFIX')
    if not TESSDATA_PREFIX:
        TESSDATA_PREFIX = "../"

    tesseract = ctypes.cdll.LoadLibrary(libname)
    tesseract.TessVersion.restype = ctypes.c_char_p
    tesseract_version = tesseract.TessVersion()
    print('Tesseract-ocr version', tesseract_version)
    api = tesseract.TessBaseAPICreate()
    rc = tesseract.TessBaseAPIInit3(api, TESSDATA_PREFIX, "h")
    if (rc):
        tesseract.TessBaseAPIDelete(api)
        print("Could not initialize tesseract.\n")
        exit(3)

    text_out = tesseract.TessBaseAPIProcessPages(api, image, None, 0)
    result_text = ctypes.string_at(text_out)

    print('Tesseract-ocr version', tesseract_version)
    print(result_text)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.base_dir)