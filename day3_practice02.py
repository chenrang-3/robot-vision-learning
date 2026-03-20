import cv2
import numpy as np

path="./za04.jpg"
img=cv2.imread(path,cv2.IMREAD_COLOR)
img_copy=img.copy()

GAUSSIAN_KERNEL=(3,3)
MEDIAN_KERNEL=3
MORPH_KERNEL_SIZE=(3,3)


if img is None:
    print("图片读取失败")
    exit()

gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gaussian_blur=cv2.GaussianBlur(gray_img,GAUSSIAN_KERNEL,0)
median_blur=cv2.medianBlur(gaussian_blur,MEDIAN_KERNEL)

#二值化：自适应阈值替代固定阈值
binary_img=cv2.adaptiveThreshold(median_blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,21,6)

kernel_open=cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
kernel_close=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))

#开运算
open_img=cv2.morphologyEx(binary_img,cv2.MORPH_OPEN,kernel_open,3)
#闭运算
close_img=cv2.morphologyEx(open_img,cv2.MORPH_CLOSE,kernel_close,2)
#膨胀
dilate_img=cv2.dilate(close_img,kernel_close,iterations=1)
morph_result=dilate_img

#找轮廓
contours,hierarchy=cv2.findContours(morph_result,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#区分导航线和障碍物
obstacle_list=[]
min_area=500
for cnt in contours:
    area=cv2.contourArea(cnt)
    if area<min_area:
        continue
    x,y,w,h=cv2.boundingRect(cnt)
    ratio=max(w,h)/min(w,h)
    if ratio<8:
        cx=x+w//2
        cy=y+h//2
        obstacle_list.append((x,y,w,h,cx,cy))

        cv2.rectangle(img_copy,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.circle(img_copy,(cx,cy),4,(255,0,0),-1)
print(f"检测到障碍物数量：{len(obstacle_list)}")
for i,(x,y,w,h,cx,cy) in enumerate(obstacle_list):
    print(f"障碍物{i}:左上({x},{y}),宽：{w}高：{h}中心：({cx},{cy})")
cv2.imshow("img",img)
cv2.imshow("morph_result",morph_result)
cv2.imshow("img_copy",img_copy)
if cv2.waitKey(0) & 0xFF==ord('q'):
    cv2.destroyAllWindows()