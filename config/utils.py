import imghdr

def substringCircum(value):
    return value.split("-")[0]

def substringSecondCircum(value):
    return value.split("-")[1]

def changeFileType(value, type):
    file_type = value.split(".")[1]
    return value.replace(file_type, type)

def checkImageSize(value):
    size = (len(value) * 3) / 4
    if(size <= 3300000): # 3mb's photo
        return True
    return False    

def checkImageType(file_dir, accepted_type):
    result = filter(lambda type : type == imghdr.what(file_dir), accepted_type)
    print(imghdr.what(file_dir))
    return len(list(result)) > 0