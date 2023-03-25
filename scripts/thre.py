import numpy as np
from PIL import Image
im_gray = np.array(Image.open('./data/input_side.jpg').convert('L'))
for i in range(0,9):
    print(type(im_gray))
    # <class 'numpy.ndarray'>
    maxval = 255
    thresh = 50+i

    im_bin = (im_gray > thresh) * maxval
    print(im_bin)
    # [[255 255 255 ... 255 255   0]
    #  [255 255 255 ... 255 255   0]
    #  [255 255 255 ... 255   0   0]
    #  ...
    #  [  0   0   0 ...   0   0   0]
    #  [  0   0   0 ...   0   0   0]
    #  [  0   0   0 ...   0   0   0]]

    Image.fromarray(np.uint8(im_bin)).save('./param/binarization/output%d.jpg' %thresh)