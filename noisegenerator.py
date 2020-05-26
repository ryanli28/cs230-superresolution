# Generates noise for images in the DICOM format to create artificially lower resolution fMRI images

from PIL import Image
from nibabel.pydicom_compat import pydicom
import numpy as np
from numpy import asarray
import os
from os import listdir
import cv2

def noisy(noise_typ, image):
    if noise_typ == "gauss":
        row,col= image.shape
        mean = 0
        var = 0.1
        sigma = var**0.5
        gauss = np.random.normal(mean,sigma,(row,col))
        gauss = gauss.reshape(row,col)
        noisy = image + image/5 * gauss
        return noisy

# loads images from one folder
def load_images(path):
    os.makedirs('fMRI_data/' + path[10] + 'l')
    os.makedirs('fMRI_data/' + path[10] + 'h')
    i = 0
    for filename in listdir(path): # enumerate file names in directory, assume all are images
        dcm = pydicom.dcmread(path + "/" + filename, force = True)
        pixels = dcm.pixel_array
        noisy_pixels = noisy("gauss", pixels)
        #gaussian = np.random.normal(0, 5, (pixels.shape[0], pixels.shape[1]))
        #gaussian = gaussian.reshape(pixels.shape[0], pixels.shape[1])
        #gaussian = gaussian.astype(np.uint8)
        #pixels = pixels + gaussian
        #cv2.normalize(pixels, pixels, 0, 511, cv2.NORM_MINMAX, dtype = -1)
        #image = Image.fromarray(pixels)
        #image = image.convert("L")
        np.save('fMRI_data/' + path[10] + 'l/' + path[10] + 'l_' + str(i) + '.npy', noisy_pixels)
        np.save('fMRI_data/' + path[10] + 'h/' + path[10] + 'h_' + str(i) + '.npy', pixels)
        #image.save('fMRI_data/' + path[10] + 'l_' + str(i) + 'a.png')
        i = i + 1

#+ filename[0:-4]
path = "fMRI_data/1-high"
load_images(path)

def generate_txt_file():
    f = open("hr_file.txt", "w+")
    i = 0
    for filename in listdir("/Users/ryanli/Desktop/mri_dataset/0h"):
        f.write("/Users/ryanli/Desktop/mri_dataset/0h" + "/0h_" + str(i) + ".npy" + "\n")
        i = i + 1
    f.close()

#generate_txt_file()