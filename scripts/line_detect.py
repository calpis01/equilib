import cv2
import numpy as np
import pickle
if __name__ == "__main__":
    length_threshold = 10
    distance_threshold = 1.414
    canny_th1 = 13
    canny_th2 = 23
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
    place = "_winn"
    for i in range(0,20):
        #1度ずつ
        img = cv2.imread("rotate_image"+place+"/output%d.jpg" %i, 0)
        f = open("line_parameter"+place+"/list%d.txt" %i, 'wb')

        #0.1度ずつ
        #img = cv2.imread("frotate"+place+"/output%d.jpg" %i, 0)
        #f = open("line_parameter"+place+"_f"+"/list%d.txt" %i, 'wb')

        #roi = (2600, 1670, 4080, 1690)
        roi = (2350, 1670, 4800, 1690) # madogawa
        s_roi = img[roi[1]:roi[3], roi[0]:roi[2]]
        lines = fld.detect(s_roi)
        if lines is None : 
            line_list = np.array([0,0,0,0])
            pickle.dump(line_list, f)
            continue
        lines[:,:,0] += roi[0]
        lines[:,:,2] += roi[0]
        lines[:,:,1] += roi[1]
        lines[:,:,3] += roi[1]
        print(i, lines.shape)
        #print(lines[:,:,0],lines[:,:,2])
        out = fld.drawSegments(img, lines)
        #line_list =
        line_list = lines[:,0,::2]
        pickle.dump(line_list, f)
        cv2.imwrite("detected"+place+"/output%d.jpg" %i, out)
        #cv2.imwrite("fdetect"+place+"/output%d.jpg" %i, out)
