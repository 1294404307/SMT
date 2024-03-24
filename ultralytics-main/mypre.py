from ultralytics import YOLO
import cv2

model=YOLO(r'D:\runs\weight\three\best100epoch.pt')

# result = model.predict(source=r'E:\pythonCode\ultralytics-main\data\images\test',show=True,save=True)
# img=cv2.imread(r'testpcb.jpg',0)
# cv2.circle(img,(200,0),5,(255,0,0))

# cv2.imshow('w',img)
# cv2.waitKey(0)
# E:\pythonCode\检测
result = model.predict(source=r'D:\pythonCode\ultralytics-main\needdetect',show=False,save=True)
# model.predict(img,show=True)