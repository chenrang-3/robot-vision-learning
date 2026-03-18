import cv2
import numpy as np

path="./diban.jpg"
img=cv2.imread(path,cv2.IMREAD_COLOR)
if img is None:
    print("读取失败")
    exit()

#高斯滤波
GAUSSIAN_KERNEL=(5,5)
#中值滤波
MEDIAN_KERNEL=3

#形态学滤波
MORPH_KERNEL_SIZE=(3,3)
#二值化阈值
THRESHOLD_VALUE=120

THRESHOLD_INVERT=True

while True:
    #彩色转灰色
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #滤波去噪
    gaussian_blur=cv2.GaussianBlur(gray,GAUSSIAN_KERNEL,0)
    median_blur=cv2.medianBlur(gaussian_blur,MEDIAN_KERNEL)
    denoised_img=median_blur

    #二值化
    threshold_type=cv2.THRESH_BINARY_INV if THRESHOLD_INVERT else cv2.THRESH_BINARY

    ret,binary_img=cv2.threshold(denoised_img,THRESHOLD_VALUE,maxval=255,type=threshold_type)

    #形态学操作
    morph_kernel=cv2.getStructuringElement(cv2.MORPH_RECT,ksize=MORPH_KERNEL_SIZE)

    #开运算去除小噪点
    open_img=cv2.morphologyEx(binary_img,cv2.MORPH_OPEN,morph_kernel,iterations=1)
    #闭运算填充小孔洞
    close_img=cv2.morphologyEx(open_img,cv2.MORPH_CLOSE,morph_kernel,iterations=1)

    morph_result=close_img.copy()
    #轮廓检测
    contours,hierachy=cv2.findContours(morph_result,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #绘制轮廓
    result_img=img.copy()
    cv2.drawContours(result_img,contours,contourIdx=-1,color=(0,255,0),thickness=2)

    cv2.imshow("1",img)
    cv2.imshow("2",denoised_img)
    cv2.imshow("3",binary_img)
    cv2.imshow("4",morph_result)
    cv2.imshow("5",result_img)

    if cv2.waitKey(0) & 0xFF==ord('q'):
        break
cv2.destroyAllWindows()