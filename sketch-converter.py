import numpy as np
import imageio.v2 as imageio  # Updated for compatibility
import scipy.ndimage
import cv2

img = "me.png"  # Ensure this image exists in the same directory

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def dodge(front, back):
    result = front * 255 / (255 - back + 1e-6)  # Add epsilon to avoid divide by zero
    result[result > 255] = 255
    result[back == 255] = 255
    return result.astype('uint8')

ss = imageio.imread(img)
gray = rgb2gray(ss)
i = 255 - gray

blur = scipy.ndimage.gaussian_filter(i, sigma=15)  # Corrected this line

r = dodge(blur, gray)

cv2.imwrite('me-sketch.png', r)
