import cv2

cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print("摄像头打开失败")
    exit()
while True:
    ret,frame=cap.read()

    #检查画面读取情况
    if not ret:
        print("画面读取失败")
        break
    height,width=frame.shape[:2]

    #小车只取重要roi区域
    roi_y_start=int(height*0.5)
    roi_y_end=height
    roi_x_start=0
    roi_x_end=width

    roi_frame=frame[roi_y_start:roi_y_end,roi_x_start:roi_x_end]

    #把BGR空间转成HSV空间
    hsv_frame=cv2.cvtColor(roi_frame,cv2.COLOR_BGR2HSV)

    #显示窗口
    cv2.imshow("1.原图",frame)
    cv2.imshow("2.半图",roi_frame)
    cv2.imshow("3.HSV图",hsv_frame)

    if (cv2.waitKey(1) & 0xFF) ==ord('q'):
        break
    #“==”优先级高于“&”，所以加括号

cap.release()

cv2.destroyAllWindows()