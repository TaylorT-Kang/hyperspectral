from readHSI import readHSI
import cv2
import numpy as np

def mouse_callback(event, x, y, flags, param):
    print('mouse evnet')

img = np.zeros((512,512,3),np.uint8)
cv2.namedWindow('image')

cv2.setMouseCallback('image',mouse_callback)

fnameHD = './2020_05_07/ADD_0507-1510.hdr'
fnameRaw = './2020_05_07/ADD_0507-1510.raw'
hsi = readHSI(fnameHD, fnameRaw)
cube, wavelength, _ = hsi.get_HSI()
S = hsi.RGBimage_HSI()
cv2.imshow('RGB_image',S)

cv2.waitKey(0)
cv2.destroyAllWindows()