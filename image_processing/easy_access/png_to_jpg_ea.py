import os
from PIL import Image

dir_read = input("./")
dir_write = input("./jpg/")
files = os.listdir(dir_read)
if len(files) == 0:
    print('No file was founded')
for file in files:
    img = Image.open(dir_read + file)
    file = file.split('.')
    if file[-1] == 'png':
        file[-1] = 'jpg'
        file = '.'.join(file)
        # notice: some png files may have alpha channel hence only rgb channel were saved
        r, g, b = img.split()[0], img.split()[1], img.split()[2]
        img = Image.merge("RGB", (r, g, b))
        img.save(dir_write + file)
