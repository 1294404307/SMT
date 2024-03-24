from ultralytics import YOLO

if __name__=='__main__':

    model = YOLO(r"D:\pythonCode\ultralytics-main\ultralytics\cfg\models\v8\myyolov8.yaml")  # build a new model from scratch
    # model = YOLO(r"E:\runs\weight\best21.30(pcbdz).pt")  # load a pretrained model (recommended for training)
    model = YOLO(r"D:\pythonCode\ultralytics-main\yolov8n.pt")  # load a pretrained model (recommended for training)

    # Use the model9/
    model.train(data=r"D:\pythonCode\ultralytics-main\ultralytics\cfg\datasets\mycoco128.yaml", epochs=60)  # train the model
    metrics = model.val()  # evaluate model performance  on the validation se t
# results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
# path = model.export(format="onnx")  # export the model to ONNX format