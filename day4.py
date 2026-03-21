import cv2

img=cv2.imread("za05.jpg",cv2.IMREAD_COLOR)
if img is None:
    print("读取失败")
    exit()

gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

blurred=cv2.GaussianBlur(gray,(5,5),0)
canny_output=cv2.Canny(blurred,threshold1=50,threshold2=150,apertureSize=3,L2gradient=False)

contours,hierarchy=cv2.findContours(canny_output,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

img_result=img.copy()
for i,contour in enumerate(contours):
    contour_area=cv2.contourArea(contour)
    if contour_area>1800:
        continue
    x,y,w,h=cv2.boundingRect(contour)
    #绘制框架
    cv2.rectangle(img_result,(x,y),(x+w,y+h),(0,255,0),2)
    #绘制轮廓
    cv2.drawContours(img_result,contours,i,(0,0,255),1)
    #标注轮廓面积
    cv2.putText(img_result,f"Area:{int(contour_area)}",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,0,0),1)
cv2.imshow("original img",img)
cv2.imshow("gaussian",blurred)
cv2.imshow("gray",gray)
cv2.imshow("canny_output",canny_output)
cv2.imshow("img_result",img_result)
if cv2.waitKey(0) & 0xFF==ord('q'):
    cv2.destroyAllWindows()