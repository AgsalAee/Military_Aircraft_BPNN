import shutil
import os


def removefile():
    try:
        shutil.rmtree("images")
        shutil.rmtree("warna")
        shutil.rmtree("results")
    except:
        print("sudah dihapus")
    try:
        os.mkdir("images")
        os.mkdir("warna")
        os.mkdir("results")
    except:
        print("sudah buat folder")
