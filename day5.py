import cv2

#加载Haar特征分类器
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
if face_cascade.empty():
    print("人脸分类器加载失败")
    exit()

img=cv2.imread("face.jpg",cv2.IMREAD_COLOR)
if img is None:
    print("图片读取失败")
    exit()

#转灰度图
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#人脸检测
faces=face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30))

result_img=img.copy()

#绘制结果
for (x,y,w,h) in faces:
    cv2.rectangle(result_img,(x,y),(x+w,y+h),(0,0,255),3)

cv2.imshow("img",img)
cv2.imshow("result_img",result_img)
if cv2.waitKey(0) % 0xFF==ord('q'):
    cv2.destroyAllWindows()