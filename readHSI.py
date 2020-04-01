import re

import numpy as np
import cv2 as cv
import array
def fread(fid, nelements, dtype):
    """Equivalent to Matlab fread function"""

    if dtype is np.str:
        dt = np.uint8  # WARNING: assuming 8-bit ASCII for np.str!
    else:
        dt = dtype

    data_array = np.fromfile(fid, dt, count=nelements)
    data_array.shape = (nelements, 1)
    return data_array


class readHSI:
    cube = 0
    bands = 0
    samples = 0
    lines = 0
    selectBand = 0
    def __init__(self,fnameHD,fnameRaw):
        self.fnameHD = fnameHD
        self.fnameRaw = fnameRaw

    def get_HSI(self):
        #load hdr file data
        f = open(self.fnameHD,'r')
        num = []
        for i in range(10):
            A_vector = f.readline()
            #print(A_vector)
        for k in range(3):
            A_vector = f.readline()
            #print(A_vector)
            A_vector = A_vector.split()
            num.append(int(A_vector[2]))
            #print(num)
        self.samples = num[0]
        self.lines = num[1]
        self.bands = num[2]
        #print(bands)
        def_bands = f.readline()

        for i in range(20):
            A_vector = f.readline()

        Wavelength = np.zeros(self.bands)
        for i in range(self.bands):
            B_vector = f.readline().split(',')
            Wavelength[i] = float(B_vector[0])
        f.close()

        bandInfo = re.findall('\d+', def_bands)
        r_band = int(bandInfo[0])
        g_band = int(bandInfo[1])
        b_band = int(bandInfo[2])
        self.selectBand = [r_band, g_band, b_band]

        #load raw file data
        f = open(self.fnameRaw, 'rb')
        numTotal = self.samples * self.bands * self.lines
        # with open(self.fnameRaw,'rb') as fid:
        #     data = np.fromfile(fid, np.uint16, numTotal,)
        data = fread(f, numTotal, 'uint16')
        f.close()
        self.cube = data.reshape(self.samples, self.bands, self.lines, order='F')
        del(data)
        for i in range(self.bands):
            R = np.squeeze(self.cube[:,i,:])
            R = np.flipud(R)
            self.cube[:,i,:] = R
        return self.cube, Wavelength, self.selectBand

    def RGBimage_HSI(self):
        bands = self.bands
        samples = self.samples
        #print(self.samples)

        lines = self.lines
        cube = self.cube
        selectBand = self.selectBand
        # for i in range(bands):
        #     R = np.squeeze(cube[:,i,:])
        #     R = np.flipud(R)
        #     cube[:,i,:] = R
        r_band = selectBand[0]
        g_band = selectBand[1]
        b_band = selectBand[2]
        R = np.squeeze(cube[:,r_band+1,:])
        G = np.squeeze(cube[:,g_band+1,:])
        B = np.squeeze(cube[:,b_band+1,:])
        S = np.zeros((samples,lines,3))
        
        S[:,:,0] = R/R.max()*255
        S[:,:,1] = G/G.max()*255
        S[:,:,2] = B/B.max()*255
        break_point = 0
        S = np.uint8(S)
        return S
