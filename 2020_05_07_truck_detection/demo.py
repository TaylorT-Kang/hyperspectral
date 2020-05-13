#%%
from readHSI import readHSI
import matplotlib.pyplot as plt
import cv2 as cv2
import numpy as np
import random
import math as math
from hyperSam import hyperSam
import struct
import pickle
def gauss1d(order,sig):
    j=0
    f=[]
    temp  = math.trunc(order/2)
    for x in range(-temp,temp+1,1):
        f.append(1/2/math.pi*math.exp(-(x**2)/(2*sig**2)))
    
    f = np.array(f)
    f = f/ sum(f)
    return f

fnameHD = './2020_05_07/ADD_0507-1510.hdr'
fnameRaw = './2020_05_07/ADD_0507-1510.raw'
# fnameHD = 'HSI_0103-1640-2.hdr'
# fnameRaw = 'HSI_0103-1640-2.raw'
hsi = readHSI(fnameHD, fnameRaw)
cube, wavelength, _ = hsi.get_HSI()
S = hsi.RGBimage_HSI()
cv2.imshow('RGB_image',S)

# ## load paint spectrum
# f = open('paint_spectrum.raw','rb')
# paint_spectrum = np.fromfile(f,dtype=np.uint16)
# paint_spectrum = paint_spectrum.reshape(12,258)
# f.close()

## load paint mean spectrum
f = open('truck_spectrum.raw','rb')
paint_spectrum = np.fromfile(f,dtype=np.float64)
paint_spectrum = paint_spectrum.reshape(12,258)
f.close()


# pixel_spectral = np.squeeze(cube[r_x,:,r_y])
# pixel_spectral2 = np.squeeze(cube[r_x2,:,r_y2])
sig = 1
order = sig * 3 * 2 + 1
f = gauss1d(order,sig)

cube_shape = cube.shape
height = cube_shape[0]
width = cube_shape[2]
threshole = np.zeros((height,width),dtype=np.uint8)


for i in range(height):
    for j in range(width):
        angle = hyperSam(paint_spectrum[2,:],cube[i,:,j]).getSam()
        if angle < 0.07:
            threshole[i,j] = 255
            for k in range(3):
                S[i,j,k] = 255

# for i in range(height):
#     for j in range(width):
#         spectrum = cube[i,:,j]
#         normalize_spectrum = (spectrum-spectrum.min()) / (spectrum.max() - spectrum.min())
#         paint_spectrum = paint_spectrum.astype(np.float64)
#         angle = hyperSam(paint_spectrum,normalize_spectrum).getSam()
#         if angle < 0.07:
#             threshole[i,j] = 255
#             S[i,j,0] = 0
#             S[i,j,1] = 0
#             S[i,j,2] = 255

cv2.imshow('truck', threshole)
cv2.imshow('find truck at RGB image', S)



# filtered_pixel_spectral = np.correlate(pixel_spectral,f,"same")
cv2.waitKey(0)
cv2.destroyAllWindows()