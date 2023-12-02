import cv2
from ultralytics import YOLO

# モデルを選択する
model = YOLO('yolov8n-seg.pt')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while cap.isOpened():
    success, frame = cap.read()

    if success:
        results = model(frame)

        #フレーム内に結果を表示
        annotated_frame = results[0].plot()

        #annotated_frameを表示する
        cv2.imshow("YOLO v8 Interface", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
