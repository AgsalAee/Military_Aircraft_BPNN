
from typing_extensions import Self
import pandas as pd
from scipy.spatial import distance


from glcm import glcm_process

# os.chdir("A:/Agsal/Belajar/Semester 8/Skripsi/contoh/Deteksi_Pesawat_BP_Backend/")


def main_euc():
    glcm = glcm_process()
    glcmresult = glcm.glcm_main(Self)
    glcmarr = glcmresult.to_numpy()

    df = pd.read_excel('distance.xlsx')
    df = df.drop(columns=df.iloc[:, 0:17])
    df = df.drop(columns=df.iloc[:, -1:])
    dfjenis = df.iloc[:, -1:]
    dfjenis = dfjenis.to_numpy()
    df1 = df.drop(columns=df.iloc[:, -1:])
    df1ar = df1.to_numpy()

    print(glcmarr[0])
    print(df1ar[0])

    check = []
    for i in range(len(df1)):
        getdist = distance.euclidean(glcmarr[0], df1ar[i])
        check.append(getdist)

    # minim = min(check)
    # ind = check.index(minim)
    # jenisnya = dfjenis[ind]
    # print(jenisnya)
    # return jenisnya

    MAX = 100000

    firstmin = MAX
    secmin = MAX
    thirdmin = MAX

    for i in range(len(df1)):

        # Check if current element
        # is less than firstmin,
        # then update first,second
        # and third

        if check[i] < firstmin:
            thirdmin = secmin
            secmin = firstmin
            firstmin = check[i]

        # Check if current element is
        # less than secmin then update
        # second and third
        elif check[i] < secmin:
            thirdmin = secmin
            secmin = check[i]

        # Check if current element is
        # less than,then update third
        elif check[i] < thirdmin:
            thirdmin = check[i]

    print("First min = ", firstmin)
    print("Second min = ", secmin)
    print("Third min = ", thirdmin)

    pertama = dfjenis[check.index(firstmin)]
    kedua = dfjenis[check.index(secmin)]
    ketiga = dfjenis[check.index(thirdmin)]
    # print(eucArr)
    # print("First min = ", pertama)
    # print("Second min = ", kedua)
    # print("Third min = ", ketiga)

    return pertama, kedua, ketiga

# # # # alternatif cara
# bestdist = 10000
# for i in range(len(df1)):
#     getdist = distance.euclidean(glcmarr[0], df1ar[i])
#     # print(getdist)
#     # print(getdist)
#     # print(bestdist)
#     if bestdist > getdist:
#         bestdist = getdist
#         print("data masuk")
#         print(bestdist)
#         # print(bestdist)
#     else:
#         print("ditolak")

# print("data terakhir")
# print(bestdist)
###


# def get_neighbors(train_data, test_data, num_neighbors):
#     distances = list()
#     for x, row in train_data.iterrows():
#         dist = distance.euclidean_distance(test_data, row['fusi_informasi'])
#         distances.append([row, dist])
#     distances.sort(key=lambda tup: tup[1])
#     neighbors = list()
#     for i in range(num_neighbors):
#         neighbors.append(distances[i][0])
#     return neighbors


# # Test distance function
# def identification(pict_feature):
#     fields = ['jenis']
#     data = pd.read_excel('A:/Agsal/Belajar/Semester 8/Skripsi/contoh/Deteksi_Pesawat_BP/distance.xlsx',
#                          skipinitialspace=True, usecols=fields)

#     row0 = pict_feature
#     neighbors = get_neighbors(data, row0, 3)
#     jenis = list()
#     for neighbor in neighbors:
#         jenis.append(neighbor['jenis'])
#     print(jenis)
#     return jenis
