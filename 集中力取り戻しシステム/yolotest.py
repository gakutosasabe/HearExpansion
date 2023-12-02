from ultralytics import YOLO

# モデルを選択
#model = YOLO("yolov8n.pt")
#model = YOLO("yolov8x.pt")
model = YOLO("yolov8n-seg.pt")

# WEBカメラからリアルタイム検出
results = model(0, show=True)
for i in enumerate(results):
    print(i)
