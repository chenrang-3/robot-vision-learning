import cv2

path="./cub.jpg"
img=cv2.imread(path)

if img is None:
    print("读取失败")
    exit()
else:
    print("读取成功！图片尺寸：",img.shape)

cv2.imshow("my imag",img)

key=cv2.waitKey(0)
if key ==ord("s"):
    cv2.imwrite("test_copy.png",img)
    print("图片保存成功")
else:
    print("图片未保存")
cv2.destroyAllWindows()