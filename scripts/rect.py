import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle
if __name__ == "__main__":
    length_threshold = 20
    distance_threshold = 1.41421356
    canny_th1 = 10
    canny_th2 = 30
    canny_aperture_size = 3
    do_merge = False
    
    fld = cv2.ximgproc.createFastLineDetector(
        length_threshold,
        distance_threshold,
        canny_th1,
        canny_th2,
        canny_aperture_size,
        do_merge
    )
    line_list = []
    for i in range(17,18):
        img = cv2.imread("./rotate_image_lab/output%d.jpg" %i)
        
        #roi = (2350, 1670, 4300, 1690)
        #roi = (2000, 1670, 4800, 1690)
        roi = (2350, 1670, 4300, 1690) 
        #dst_img = img.copy()
        s_roi = img[roi[1]:roi[3], roi[0]:roi[2]]
        #lines = fld.detect(s_roi)
        #lines[:,:,0] += roi[0]
        #lines[:,:,2] += roi[0]
        #lines[:,:,1] += roi[1]
        #lines[:,:,3] += roi[1]
        #print(i, lines.shape)
        #print(lines[:,:,0],lines[:,:,2])
        #out = fld.drawSegments(img, lines)
        #line_list =
        #line_list = lines[:,0,::2]
        rect_img = img.copy()
        change_param_name = "orientation"
        cv2.rectangle(rect_img, (roi[2],roi[3]), (roi[0],roi[1]), (0, 255, 0), 3)
        cv2.imwrite("rect/inputa%d.jpg" %i, rect_img)