from typing_extensions import Self
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import math
import pandas as pd
import imutils.paths as path


class glcm_process:
    def export(self):
        PATH = 'warna/'
        imagePath = sorted(list(path.list_images(PATH)))
        return imagePath

    def derajat0(self, img):
        max = np.max(img)
        imgTmp = np.zeros([max+1, max+1])
        for i in range(len(img)):
            for j in range(len(img[i])-1):
                imgTmp[img[i, j], img[i, j+1]] += 1

        transpos = np.transpose(imgTmp)
        data = imgTmp+transpos

        tmp = 0
        for i in range(len(data)):
            for j in range(len(data)):
                tmp += data[i, j]

        for i in range(len(data)):
            for j in range(len(data)):
                data[i, j] /= tmp
        return data

    def derajat45(self, img):
        max = np.max(img)
        imgTmp = np.zeros([max+1, max+1])
        for i in range(len(img)-1):
            for j in range(len(img[i])-1):
                imgTmp[img[i+1, j], img[i, j+1]] += 1

        transpos = np.transpose(imgTmp)
        data = imgTmp+transpos

        tmp = 0
        for i in range(len(data)):
            for j in range(len(data)):
                tmp += data[i, j]

        for i in range(len(data)):
            for j in range(len(data)):
                data[i, j] /= tmp
        return data

    def derajat90(self, img):
        max = np.max(img)
        imgTmp = np.zeros([max+1, max+1])
        for i in range(len(img)-1):
            for j in range(len(img[i])):
                imgTmp[img[i+1, j], img[i, j]] += 1

        transpos = np.transpose(imgTmp)
        data = imgTmp+transpos

        tmp = 0
        for i in range(len(data)):
            for j in range(len(data)):
                tmp += data[i, j]

        for i in range(len(data)):
            for j in range(len(data)):
                data[i, j] /= tmp
        return data

    def derajat135(self, img):
        max = np.max(img)
        imgTmp = np.zeros([max+1, max+1])
        for i in range(len(img)-1):
            for j in range(len(img[i])-1):
                imgTmp[img[i, j], img[i+1, j+1]] += 1

        transpos = np.transpose(imgTmp)
        data = imgTmp+transpos

        tmp = 0
        for i in range(len(data)):
            for j in range(len(data)):
                tmp += data[i, j]

        for i in range(len(data)):
            for j in range(len(data)):
                data[i, j] /= tmp
        return data

    def contras(self, data):
        contras = 0
        for i in range(len(data)):
            for j in range(len(data)):
                contras += data[i, j]*pow(i-j, 2)
        return contras

    def entropy(self, data):
        entro = 0
        for i in range(len(data)):
            for j in range(len(data)):
                if data[i, j] > 0.0:
                    entro += -(data[i, j]*math.log(data[i, j]))
        return entro

    def homogenitas(self, data):
        homogen = 0
        for i in range(len(data)):
            for j in range(len(data)):
                homogen += data[i, j]*(1+(pow(i-j, 2)))
        return homogen

    def energi(self, data):
        energi = 0
        for i in range(len(data)):
            for j in range(len(data)):
                energi += data[i, j]**2
        return energi

    def glcm_main(self, data):
        imagePath = self.export()
        data = []
        for i in imagePath:
            img = cv.imread(i)
            img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            data.append(img)

        hasil = []
        for i in range(len(data)):
            dat = []
            dat.append(self.derajat0(data[i]))
            dat.append(self.derajat45(data[i]))
            dat.append(self.derajat90(data[i]))
            dat.append(self.derajat135(data[i]))
            hasil.append(dat)

        hasilnya = []
        fusi_energy = 0
        fusi_homogenitas = 0
        fusi_entropy = 0
        fusi_contras = 0
        for j in range(len(hasil)):
            da = []
            da.append(imagePath[j])
            for i in hasil[j]:
                den = self.energi(i)
                da.append(den)

                dh = self.homogenitas(i)
                da.append(dh)

                dtr = self.entropy(i)
                da.append(dtr)

                dc = self.contras(i)
                da.append(dc)

                fusi_energy += den
                fusi_homogenitas += dh
                fusi_entropy += dtr
                fusi_contras += dc

            hasilnya.append(da)
            da.append(fusi_energy)
            da.append(fusi_homogenitas)
            da.append(fusi_entropy)
            da.append(fusi_contras)

        resultable = ['file', 'energy_0', 'homogenity_0', 'entrophy_0', 'contrast_0', 'energy_45', 'homogenity_45', 'entrophy_45', 'contrast_45', 'energy_90', 'homogenity_90',
                      'entrophy_90', 'contrast_90', 'energy_135', 'homogenity_135', 'entrophy_135', 'contrast_135', 'fusi_energy', 'fusi_homogenity', 'fusi_entrophy', 'fusi_contrast']
        dp = pd.DataFrame(hasilnya, columns=resultable)

        feature_cols = ["fusi_energy", "fusi_homogenity",
                        "fusi_entrophy", "fusi_contrast"]
        fusinya = dp[feature_cols]

        return fusinya


if __name__ == "__main__":
    glcm_process().glcm_main(Self)


#         toarr = fusinya.to_numpy()
#         print(toarr)

# #        #mencari standart scaller untuk 1 Dimensi array#
#         # scaler = StandardScaler()
#         # ScFusinya = scaler.fit_transform(toarr)
#         # fusinya = pd.DataFrame(ScFusinya, columns=feature_cols)
#         StdScFusi = preprocessing.normalize(fusinya)
#         fusinya = pd.DataFrame(StdScFusi, columns=feature_cols)

    # fusinya.to_excel('fusinya.xlsx', index=False)
    # def print_glcm():
    #     dx = glcm_main()
    #     dx.to_excel('test1.xlsx', index=False)
    # return dx

    # def exampleprint(da):
    #     resultable = ['file', 'energy_0', 'homogenity_0', 'entrophy_0', 'contrast_0', 'energy_45', 'homogenity_45', 'entrophy_45', 'contrast_45', 'energy_90', 'homogenity_90',
    #                   'entrophy_90', 'contrast_90', 'energy_135', 'homogenity_135', 'entrophy_135', 'contrast_135', 'fusi_energy', 'fusi_homogenity', 'fusi_entrophy', 'fusi_contrast']
    #     df = pd.DataFrame(da, columns=resultable)
    #     df.to_csv('ekstraksicsv.csv', index=False)
