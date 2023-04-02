from skimage.transform import warp
from skimage.transform import SimilarityTransform
import numpy as np
from PIL import Image
import cv2
import os.path as osp
def rotate_panorama(image, angle):
    """全天球パノラマ画像を回転する関数"""
    
    # 回転角度から回転行列を生成する
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                                [np.sin(angle), np.cos(angle), 0],
                                [0, 0, 1]])
    
    # 回転行列を用いて回転変換を定義する
    tform = SimilarityTransform(rotation_matrix)
    
    # 回転変換を適用する
    rotated_image = warp(image, tform, mode='wrap')
    
    return rotated_image

src_img = cv2.imread("output0.jpg")
output_img = rotate_panorama(src_img, 90)
cv2.imwrite("test.jpg", output_img)
