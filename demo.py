#%%
from readHSI import readHSI
import matplotlib.pyplot as plt
import cv2 as cv2
import numpy as np
import random
import math as math
from hyperSam import hyperSam
def gauss1d(order,sig):
    j=0
    f=[]
    temp  = math.trunc(order/2)
    for x in range(-temp,temp+1,1):
        f.append(1/2/math.pi*math.exp(-(x**2)/(2*sig**2)))
    
    f = np.array(f)
    f = f/ sum(f)
    return f

fnameHD = './2020_03_23/HSI_0323-1439.hdr'
fnameRaw = './2020_03_23/HSI_0323-1439.raw'
# fnameHD = 'HSI_0103-1640-2.hdr'
# fnameRaw = 'HSI_0103-1640-2.raw'
hsi = readHSI(fnameHD, fnameRaw)
cube, wavelength, _ = hsi.get_HSI()
S = hsi.RGBimage_HSI()
plt.figure(1)
#cv2.imshow("casdf",S)
plt.imshow(S)
break_point = 0
plt.savefig('HSI_RGB.jpg')
rct = [50,208,43,41]
S_crop = S[rct[1]:rct[1]+rct[3],rct[0]:rct[0]+rct[2],:]
plt.figure(2)
plt.imshow(np.uint(S_crop))
plt.savefig('cropped image.jpg')

# r_x = random.randrange(rct[1],rct[1]+rct[3])
# r_y = random.randrange(rct[0],rct[0]+rct[2])

# r_x2 = random.randrange(rct[1],rct[1]+rct[3])
# r_y2 = random.randrange(rct[0],rct[0]+rct[2])

r_x = 0
r_y = 0

r_x2 = 0
r_y2 = 0

pixel_spectral = np.squeeze(cube[r_x,:,r_y])
pixel_spectral2 = np.squeeze(cube[r_x2,:,r_y2])
plt.figure(3)
sig = 1
order = sig * 3 * 2 + 1
f = gauss1d(order,sig)
# print(pixel_spectral)
# print(pixel_spectral2)

filtered_pixel_spectral = np.correlate(pixel_spectral,f,"same")

filtered_pixel_spectral2 = np.correlate(pixel_spectral2,f,"same")
plt.plot(wavelength,filtered_pixel_spectral)
plt.plot(wavelength,filtered_pixel_spectral2)
result = hyperSam(pixel_spectral,pixel_spectral2)
result = result.getSam()
print(result)
