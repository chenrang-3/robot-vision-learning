import cv2
import numpy as np

img=cv2.imread("cub.jpg",cv2.IMREAD_COLOR)
template=cv2.imread("pipei.jpg",cv2.IMREAD_GRAYSCALE)
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
template=cv2.resize(template,(150,500))

h,w=template.shape[:2]

#进行模板匹配
res=cv2.matchTemplate(gray,template,cv2.TM_CCOEFF_NORMED)

threshold=0.8
loc=np.where(res>=threshold)

#标记匹配位置
for x in zip(*loc[::-1]):
    cv2.rectangle(img,x,(x[0]+w,x[1]+h),(0,2555,0),2)
cv2.imshow("Result",gray)
if cv2.waitKey(0) & 0xFF==ord('q'):
    cv2.destroyAllWindows()