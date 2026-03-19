import cv2
import numpy as np

path="./3.jpg"
img=cv2.imread(path,cv2.IMREAD_COLOR)
if img is None:
    print("图片读取失败")
    exit()

GAUSSIAN_KERNEL=(3,3)
MEDIAN_KERNEL=3
MORPH_KERNEL_SIZE=(3,3)
THRESHOLD_VALUE=127
THRESHOLD_INVERT=True

gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gaussian_blur=cv2.GaussianBlur(gray,GAUSSIAN_KERNEL,0)

median_blur=cv2.medianBlur(gaussian_blur,MEDIAN_KERNEL)

denoised_img=median_blur

threshold_type=cv2.THRESH_BINARY_INV if THRESHOLD_INVERT else cv2.THRESH_BINARY

ret,binary_img=cv2.threshold(denoised_img,THRESHOLD_VALUE,maxval=255,type=threshold_type)
#开闭运算
MORPH_KERNEL_OPEN=(3,3)
MORPH_KERNEL_CLOSE=(11,11)

kernel_open=cv2.getStructuringElement(cv2.MORPH_RECT,MORPH_KERNEL_OPEN)
kernel_close=cv2.getStructuringElement(cv2.MORPH_RECT,MORPH_KERNEL_CLOSE)
open_img=cv2.morphologyEx(binary_img,cv2.MORPH_OPEN,kernel_open,1)
close_img=cv2.morphologyEx(open_img,cv2.MORPH_CLOSE,kernel_close,3)

morph_img=close_img
contours, hierarchy = cv2.findContours(morph_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 过滤面积过小的轮廓（小黑点）
min_contour_area = 170  # 可根据实际调整，数值越小保留细节越多
filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

# 只绘制过滤后的大轮廓（导航线）
result_img = img.copy()
cv2.drawContours(result_img, filtered_contours, -1, (0, 255, 0), 2)

h,w=morph_img.shape[:2]
scan_line_y=h-5
row=morph_img[scan_line_y,:]
white_x_indices=np.where(row==255)[0]
if len(white_x_indices)>0:
    line_center_x=np.mean(white_x_indices)
    frame_center_x=w/2
    error=line_center_x-frame_center_x
    #输出结果
    print(f"画面宽度：{w}")
    print(f"画面中心x：{frame_center_x}")
    print(f"导航中心线x:{line_center_x}")
    print(f"偏差值：{error:.1f}")
else:
    print("未检测到导航线")

cv2.imshow("original",img)
cv2.imshow("Result",result_img)
cv2.imshow("binary",binary_img)
cv2.imshow("open",open_img)
cv2.imshow("close",close_img)

if cv2.waitKey(0) & 0xFF==ord('q'):
    cv2.destroyAllWindows()