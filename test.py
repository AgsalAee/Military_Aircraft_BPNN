from ast import Try
from json import load
import os

from typing_extensions import Self
import numpy as np
from Remove_Background_BW_and_Warna import remove_background
import euclidean
from glcm import glcm_process
from keras.models import load_model
import pandas as pd
import euclidean
import shutil


# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# # #If the line below doesn't work, uncomment this line (make sure to comment the line below); it should help.
# # os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'


def test_main(file_name):
    global totArr
    totArr = []
    filename = 'NNModel/StdScMulticlass431BW.h5'
    scaler = 'NNModel/StdScaler431BW.pkl'
    feature_cols = ["fusi_energy", "fusi_homogenity",
                    "fusi_entrophy", "fusi_contrast"]
    removeBg = remove_background()
    removeBg.bg_main(file_name)
    glcm = glcm_process()
    glcmresult = glcm.glcm_main(Self)

    def scaled(Self):
        import pickle
        load_scaler = pickle.load(open(scaler, 'rb'))
        scaled = load_scaler.transform(glcmresult)
        X_scaled = pd.DataFrame(scaled, columns=feature_cols)
        totArr.append(list(scaled))
        return X_scaled

    def main(self):
        model = load_model(filename)
        pred = model.predict(scaled(Self))
        X_pred = np.argmax(pred[0])

        if X_pred == 1:
            x_pred = "attacker"
        else:
            x_pred = "fighter"
        totArr.append(x_pred)
        totArr.append(list(euclidean.main_euc()))
        return x_pred
    main(Self)

    fusi = list()
    for fs in totArr[0]:
        f_dict = {"energy": '%.4f' % fs[0], "homogenity": '%.4f' %
                  fs[1], "entrophy": '%.4f' % fs[2], "contrast": '%.4f' % fs[3]}
        fusi.append(f_dict)

    euclid = list()
    for eu in totArr[2]:
        euclid.append(eu[0])

    result = {
        "fusi": fusi.pop(),
        "classification": totArr[1],
        "euclidian": euclid,
    }

    return result


if __name__ == "__main__":
    test_main()
