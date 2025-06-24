import torch
from ultralytics import YOLO

def main():
    best_device = 'mps' if torch.mps.is_available() else 'cuda' if torch.cuda.is_available() else 'cpu'

    model = YOLO("yolo11n.pt").half()

    model.export(format='onnx', half=True, device=best_device)
    model.export(format='engine', half=True, device=best_device)

if __name__ == '__main__':
    main()