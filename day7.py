import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# 检查分类器是否加载成功
if face_cascade.empty():
    raise IOError("无法加载人脸检测分类器")

cap = cv2.VideoCapture(0)  
tracking = False  
track_window = None  
roi_hist = None  
# CamShift算法
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
while True:
    # 读取摄像头帧
    ret, frame = cap.read()
    if not ret:  
        break
    
    # 水平翻转画面
    frame = cv2.flip(frame, 1)
    # 转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if not tracking:
        # 检测人脸
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) > 0:
            # 取第一个检测到的人脸作为跟踪目标
            x, y, w, h = faces[0]
            track_window = (x, y, w, h) 
            
            # 提取人脸区域ROI
            roi = frame[y:y+h, x:x+w]
            # 转换为HSV颜色空间
            hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            # 生成掩码：过滤低亮度/低饱和度区域，减少背景干扰
            mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
            # 计算人脸区域的HSV 
            roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
            # 归一化直方图到0-255范围
            cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
            tracking = True
            cv2.putText(frame, 'Tracking Start', (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)
        pts = cv2.boxPoints(ret)
        pts = np.intp(pts)
        cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
        cv2.putText(frame, 'Tracking Face', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Face Tracking with CamShift', frame)
    key = cv2.waitKey(30) & 0xFF
    if key == 27:
        break
    # 按'r'键重置跟踪状态，重新检测人脸
    if key == ord('r'):
        tracking = False

cap.release()  
cv2.destroyAllWindows()  