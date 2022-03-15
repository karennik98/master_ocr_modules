import warnings
import os
import matplotlib.pyplot  as plt
from skimage import color
from skimage import io
import ocrodeg
import shutil
import cv2

pi=3.14

def get_sub_folder(folder):
    return [os.path.join(folder, o) for o in os.listdir(folder)
     if os.path.isdir(os.path.join(folder, o))]

def get_files(folder):
    files = list()
    all_files = os.listdir(folder)
    for image in all_files:
        if(image.endswith(".tif") or image.endswith(".jpg") or image.endswith(".jpeg")):
            image_info = os.path.splitext(image)
            for txt in all_files:
                file_info = os.path.splitext(txt)
                if "gt" in file_info[0]:
                    file_info2 = os.path.splitext(file_info[0])
                    if image_info[0] == file_info2[0] and "txt" in txt:
                        files.append((folder + '/' + image, folder + '/' + txt))
    print(len(files))
    for el in files:
        print(el)
    print("----------------------------------")
    return files

def get_file_name(file_path):
    return os.path.basename(file_path)

def pi_transform(image, angle=-1):
    return ocrodeg.transform_image(image, angle=angle*pi/180)

def transform(image, aniso=1.5):
    return ocrodeg.transform_image(image, aniso=aniso)

def printlike_multiscale(image):
    return ocrodeg.printlike_multiscale(image)

def random_blotches(image):
    return ocrodeg.random_blotches(image, 3e-4, 1e-4)

def printlike_fibrous(image):
    return ocrodeg.printlike_fibrous(image)

output_folder = "48_hy_deg_dataset"
folders = get_sub_folder('48_hy_dataset')
for folder in folders:
    file_index = 0
    out_folder = folder.replace('48_hy_dataset', '48_hy_deg_dataset')
    os.mkdir(out_folder)
    img_txt_files = get_files(folder)
    for files in img_txt_files:
        shutil.copyfile(files[1], out_folder + '/' + str(file_index) + ".gt.txt")
        imgGray = color.rgb2gray(io.imread(files[0]))
        # cv2.imwrite(out_folder + '/' + str(file_index) + '.jpg', imgGray)
        plt.imsave(out_folder + '/' + str(file_index) + '.jpg', imgGray, cmap='gray')
        file_index += 1

        shutil.copyfile(files[1], out_folder + '/' + str(file_index) + ".gt.txt")
        image1 = transform(imgGray)
        # cv2.imwrite(out_folder + '/' + str(file_index) + '.jpg', image1)
        plt.imsave(out_folder + '/' + str(file_index) + '.jpg', image1, cmap='gray')
        file_index += 1

        shutil.copyfile(files[1], out_folder + '/' + str(file_index) + ".gt.txt")
        image2 = printlike_multiscale(imgGray)
        # cv2.imwrite(out_folder + '/' + str(file_index) + '.jpg', image2)
        plt.imsave(out_folder + '/' + str(file_index) + '.jpg', image2, cmap='gray')
        file_index += 1

        shutil.copyfile(files[1], out_folder + '/' + str(file_index) + ".gt.txt")
        image3 = random_blotches(imgGray)
        # cv2.imwrite(out_folder + '/' + str(file_index) + '.jpg', image3)
        plt.imsave(out_folder + '/' + str(file_index) + '.jpg', image3, cmap='gray')
        file_index += 1

        shutil.copyfile(files[1], out_folder + '/' + str(file_index) + ".gt.txt")
        image4 = printlike_fibrous(imgGray)
        # cv2.imwrite(out_folder + '/' + str(file_index) + '.jpg', image4)
        plt.imsave(out_folder + '/' + str(file_index) + '.jpg', image4, cmap='gray')
        file_index += 1

# cmap='gray'

# img = io.imread('48_hy_dataset/ArialUnicodeMS/0.tif')
# imgGray = color.rgb2gray(img)

# for i, angle in enumerate([0, 90, 180, 270]):
#     plt.subplot(2, 2, i+1)
#     plt.imshow(ndi.rotate(image, angle))


# for i, angle in enumerate([-2, -1, 0, 1]):
#     plt.imshow(ocrodeg.transform_image(imgGray, angle=angle*pi/180))

# index = 0
# for i, aniso in enumerate([0.5, 1.0, 1.5, 2.0]):
#     tr_image = ocrodeg.transform_image(imgGray, aniso=aniso)
#     plt.imsave("image{}.jpg".format(index), tr_image)
#     index+=1


# plt.imshow(ocrodeg.printlike_multiscale(imgGray))

# blotched = ocrodeg.random_blotches(imgGray, 3e-4, 1e-4)
# plt.imshow(blotched)

# plt.imshow(ocrodeg.make_fibrous_image((256, 256), 700, 300, 0.01))

# plt.imshow(ocrodeg.printlike_fibrous(imgGray))

# noisy = ocrodeg.make_multiscale_noise_uniform((512, 512))
# plt.imshow(noisy)

# for i, sigma in enumerate([1.0, 2.0, 5.0, 20.0]):
#     noise = ocrodeg.bounded_gaussian_noise(imgGray.shape, sigma, 5.0)
#     distorted = ocrodeg.distort_with_noise(imgGray, noise)
#
#     plt.imshow(distorted)
