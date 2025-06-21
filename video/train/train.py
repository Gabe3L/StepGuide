import torch
from ultralytics import YOLO

def main():
    best_device = 'mps' if torch.mps.is_available() else 'cuda' if torch.cuda.is_available() else 'cpu'

    model = YOLO("yolo11n.pt").half()

    model.train(
        device=best_device,
        data="coco.yaml",
        project="runs",
        epochs=50,
        imgsz=640,
        batch=16,
        workers=4,
        optimizer='Adam',
        exist_ok=True
    )

    metrics = model.val(device=best_device)
    print(metrics)

    model.export(format='onnx', half=True, device=best_device)
    model.export(format='engine', half=True, device=best_device)

if __name__ == '__main__':
    main()