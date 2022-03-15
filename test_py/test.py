import os

from tesserocr import PyTessBaseAPI
from jiwer import wer
import xlsxwriter
import pereprocess

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
    files_with_paths = list()
    for file in files:
        filename = os.path.splitext(os.path.basename(file))[0]
        files_with_paths.append((filename, folder + '/' + file))
    return files_with_paths


def ocr(images, out_folder):
    ocr_results = list()
    with PyTessBaseAPI() as api:
        for img in images:
            api.Init("/home/karen/master-ocr/ocr-test/", lang=lang)
            api.SetImageFile(img[1])
            ocr_text = api.GetUTF8Text()

            file_path = out_folder + '/' + img[0] + '.txt'
            file = open(file_path ,'w+')
            file.write(ocr_text)
            file.close()

            print('filename: ', img[0])
            print('file_path: ', file_path)

            ocr_results.append((img[0], file_path))

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
    output_folder = 'ocr_texts_' + lang
    if not os.path.exists(output_folder):
        print("Creating output folder: ", output_folder)
        os.mkdir(output_folder)

    images = read_files('data/test_jpgs')
    original_files = read_files('data/original_texts')

    ocr_result = list()
    if len(read_files(output_folder)) is not len(original_files):
        ocr_result = ocr(images, output_folder)
    else:
        ocr_result = read_files(output_folder)

    wer_error_result = wer_test(original_files, ocr_result)

    write_sheet(wer_error_result)

