import os

from tesserocr import PyTessBaseAPI
from jiwer import wer
import xlsxwriter
import pereprocess

import pytesseract
from PIL import Image

import subprocess

lang = 'hye'

def write_sheet(result):
    workbook = xlsxwriter.Workbook('wer_' + lang + '.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0
    for name, score in result:
        worksheet.write(row, col, name + '.jpg')
        worksheet.write(row, col + 1, score)
        row += 1

    workbook.close()

def read_files(folder):
    files = os.listdir(folder)
    txt_files_with_paths = list()
    image_files_with_paths = list()
    txt_img_pairs = list()
    for file in files:
        filename = os.path.splitext(os.path.basename(file))[0]
        if ".gt" in filename:
            filename = filename.replace(".gt","")
            txt_files_with_paths.append((filename, folder + '/' + file))
        else:
            image_files_with_paths.append((filename, folder + '/' + file))
    for txt in txt_files_with_paths:
        for img in image_files_with_paths:
            if txt[0] == img[0]:
                txt_img_pairs.append((txt[1], img[1]))
    return txt_img_pairs

def read_subdirs(dir):
    return [f.path for f in os.scandir(dir) if f.is_dir()]


def ocr(image):
    # with PyTessBaseAPI() as api:
    #     api.Init("/home/karen/master-ocr/ocr-test/", lang=lang)
    #     api.SetImageFile(image)
    #     return api.GetUTF8Text()
    # return pytesseract.image_to_string(Image.open(image), lang=lang)

    # tesseract image_path text_result.txt -l eng
    p = subprocess.Popen(['tesseract', image, 'temp', '-l', lang], stdout=subprocess.PIPE,
    stderr = subprocess.PIPE)
    out, err = p.communicate()
    print(err)
    file  = open("temp.txt", 'r')
    line = file.readline()
    file.close()
    os.remove("temp.txt")
    return line


def wer_test(original_files, ocr_files):
    wer_error_results = list()
    for orig in original_files:
        orig_file = open(orig[1], 'r')
        ortxt = orig_file.read()
        orig_txt = pereprocess.preprocess_text(ortxt)
        orig_file.close()

        for ocr_t in ocr_files:
            if ocr_t[0] == orig[0]:
                ocr_file = open(ocr_t[1], 'r')
                octxt = ocr_file.read()
                ocr_txt = pereprocess.preprocess_text(octxt)
                ocr_file.close()

                error = wer(orig_txt, ocr_txt)
                wer_error_results.append((orig[0], round(error*100, 3)))

    return wer_error_results

if __name__ == '__main__':
    out_base_folder_name = "out"
    os.mkdir(out_base_folder_name)

    pix_dirs = read_subdirs("./test_dataset")

    # create pix subdirectories
    for pix_dir in pix_dirs:
        pix_dir = pix_dir.replace("test_dataset", out_base_folder_name)
        os.mkdir(pix_dir)

    nois_dirs_list = list()
    for pix_dir in pix_dirs:
        nois_dirs_list.append(read_subdirs(pix_dir))

    # create noise subdirectories
    for noise_dir_by_pix in nois_dirs_list:
        for noise_dir in noise_dir_by_pix:
            noise_dir = noise_dir.replace("test_dataset", out_base_folder_name)
            os.mkdir(noise_dir)

    fonts_dir = list()
    for noise_dir_by_pix in nois_dirs_list:
        for noise_dir in noise_dir_by_pix:
            fonts_dir.append(read_subdirs(noise_dir))

    font_files_pair = list()
    for font_noise in fonts_dir:
        for font in font_noise:
            font_files_pair.append((font,read_files(font)))

    out_paths = list()
    for out_i in font_files_pair:
        lst = list(out_i)
        lst[0] = lst[0].replace("test_dataset", out_base_folder_name)
        out_i = tuple(lst)
        # create font subdirectory
        os.mkdir(out_i[0])
        out_paths.append(out_i)

    for out_i in out_paths:
        orig_lines = open(out_i[0] + '/orig_lines.txt', 'w')
        ocr_lines = open(out_i[0] + '/ocr_lines.txt', 'w')
        for pairs in out_i[1]:
            it_txt = open(pairs[0], 'r')
            orig_line = it_txt.readline()

            ocr_line = ocr(pairs[1])

            orig_lines.write(orig_line)
            ocr_lines.write(ocr_line)
        print(out_i[0] + '/orig_lines.txt')
        orig_lines.close()
        ocr_lines.close()


    # print(out_paths[0][0])
    # out_paths[0][0] = out_paths[0][0].replace("test_dataset", "out")
    # print(out_paths[0][0])
    # os.mkdir(out_paths[0][0])

    # print(font_files_pair)

    # output_folder = 'ocr_texts_' + lang
    # if not os.path.exists(output_folder):
    #     print("Creating output folder: ", output_folder)
    #     os.mkdir(output_folder)
    #
    # images = read_files('data/test_jpgs')
    # original_files = read_files('data/original_texts')
    #
    # ocr_result = list()
    # if len(read_files(output_folder)) is not len(original_files):
    #     ocr_result = ocr(images, output_folder)
    # else:
    #     ocr_result = read_files(output_folder)
    #
    # wer_error_result = wer_test(original_files, ocr_result)
    #
    # write_sheet(wer_error_result)

