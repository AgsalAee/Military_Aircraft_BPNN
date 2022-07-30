
from typing_extensions import Self
from PIL import Image as Img
from config.utils import changeFileType
import numpy as np
# from U2Net.u2net_test import removeBg
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
import os
import shutil

# import sys
# sys.path.insert(1, 'A:\Agsal\Belajar\Semester 8\Skripsi\contoh\Deteksi_Pesawat_BP\U-2-Net')
from u2net_test import Background
# os.chdir("U2Net/")
# importlib.reload(u2net_test)


class remove_background:

    def bg_main(self, file_name):

        bg = Background()
        bg.main()
        # for 1 folder
        result_png = changeFileType(file_name, "png")
        image_dir = "images/"
        THRESHOLD = 0.4
        RESCALE = 255
        LAYER = 2
        COLOR = (0, 0, 0)
        THICKNESS = 4
        SAL_SHIFT = 100

        # for name in names:
        #     if name == '.ipynb_checkpo':
        #         continue
        output = load_img('results/'+result_png)
        out_img = img_to_array(output)
        out_img /= RESCALE

        out_img[out_img > THRESHOLD] = 1
        out_img[out_img <= THRESHOLD] = 0

        shape = out_img.shape
        a_layer_init = np.ones(shape=(shape[0], shape[1], 1))
        mul_layer = np.expand_dims(out_img[:, :, 0], axis=2)
        a_layer = mul_layer*a_layer_init
        rgba_out = np.append(out_img, a_layer, axis=2)

        input = load_img('images/'+file_name)
        inp_img = img_to_array(input)
        inp_img /= RESCALE

        a_layer = np.ones(shape=(shape[0], shape[1], 1))
        rgba_inp = np.append(inp_img, a_layer, axis=2)

        rem_back = (rgba_inp*rgba_out)
        rem_back_scaled = rem_back*RESCALE

        result_img = Img.fromarray(rem_back_scaled.astype('uint8'), 'RGBA')
        convert_img = result_img.convert('RGB')
        convert_img.save('warna/'+file_name)
        print('convert', file_name)

        # glcm = glcm_process()
        # return glcm

    if __name__ == "__main__":
        bg_main(Self)
