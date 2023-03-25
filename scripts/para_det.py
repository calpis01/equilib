import cv2
import numpy as np
import pickle
if __name__ == "__main__":
    
    for i in range(1,30):
        change_param_name = "canny_th"
        length_threshold = 4
        distance_threshold = 2.0
        canny_th1 = i
        canny_th2 = i+10
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
    
        img = cv2.imread("rotate_image_door/output18.jpg", 0)
        #roi = (2000, 1670, 4800, 1690)
        roi = (2350, 1670, 4300, 1700)
        #dst_img = img.copy()
        s_roi = img[roi[1]:roi[3], roi[0]:roi[2]]
        lines = fld.detect(s_roi)
        lines[:,:,0] += roi[0]
        lines[:,:,2] += roi[0]
        lines[:,:,1] += roi[1]
        lines[:,:,3] += roi[1]
        print(i, lines.shape)
        #print(lines[:,:,0],lines[:,:,2])
        out = fld.drawSegments(img, lines)
        #line_list =
        line_list = lines[:,0,::2]
        cv2.imwrite("param/"+change_param_name+"/output%d.jpg" %i, out)