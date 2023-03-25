#画像の3値化_ブログ
import cv2

#元画像の読み込み
img=cv2.imread('./data/input_side.jpg',0)
#元画像を表示
cv2.imshow("original",img)

#画像の縦の画素数、横の画素数を取得
height,width=img.shape

#３値化に使う低い側の閾値を決める
th_low_value=100
#３値化に使う高い側の閾値を決める
th_high_value=150
#3値化の白黒以外の色
gray=100

#画像の３値化
for i in range(height):
    if i % 10 == 0:
        print(i)
    for j in range(width):
        if img[i,j]<th_low_value:
            img[i,j]=0
        elif th_low_value <= img[i,j] <=th_high_value:
            img[i,j]=gray
        else :
            img[i,j]=255


#3値化した画像の表示
cv2.imshow("OpenCV",img)
cv2.imwrite("thresholding.jpg",img)
cv2.waitKey(0)
cv2.destroyAllWindows()