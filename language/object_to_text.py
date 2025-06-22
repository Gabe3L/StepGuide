from typing import Dict, Tuple, Optional, List

CONFIDENCE_THRESHOLD: float = 0.5

OBJECT_SIZES = [
    {"name": "person", "width": 60, "height": 160},
    {"name": "bicycle", "width": 150, "height": 100},
    {"name": "car", "width": 180, "height": 120},
    {"name": "motorcycle", "width": 160, "height": 100},
    {"name": "airplane", "width": 300, "height": 150},
    {"name": "bus", "width": 300, "height": 200},
    {"name": "train", "width": 400, "height": 150},
    {"name": "truck", "width": 250, "height": 150},
    {"name": "boat", "width": 140, "height": 100},
    {"name": "traffic light", "width": 30, "height": 90},
    {"name": "fire hydrant", "width": 40, "height": 70},
    {"name": "stop sign", "width": 60, "height": 60},
    {"name": "parking meter", "width": 30, "height": 100},
    {"name": "bench", "width": 120, "height": 60},
    {"name": "bird", "width": 60, "height": 40},
    {"name": "cat", "width": 80, "height": 60},
    {"name": "dog", "width": 100, "height": 80},
    {"name": "horse", "width": 160, "height": 120},
    {"name": "sheep", "width": 140, "height": 100},
    {"name": "cow", "width": 180, "height": 120},
    {"name": "elephant", "width": 220, "height": 160},
    {"name": "bear", "width": 200, "height": 150},
    {"name": "zebra", "width": 200, "height": 140},
    {"name": "giraffe", "width": 150, "height": 300},
    {"name": "backpack", "width": 50, "height": 70},
    {"name": "umbrella", "width": 60, "height": 80},
    {"name": "handbag", "width": 50, "height": 60},
    {"name": "tie", "width": 20, "height": 60},
    {"name": "suitcase", "width": 70, "height": 90},
    {"name": "frisbee", "width": 60, "height": 60},
    {"name": "skis", "width": 120, "height": 30},
    {"name": "snowboard", "width": 100, "height": 40},
    {"name": "sports ball", "width": 50, "height": 50},
    {"name": "kite", "width": 100, "height": 100},
    {"name": "baseball bat", "width": 20, "height": 80},
    {"name": "baseball glove", "width": 50, "height": 50},
    {"name": "skateboard", "width": 100, "height": 40},
    {"name": "surfboard", "width": 120, "height": 40},
    {"name": "tennis racket", "width": 50, "height": 80},
    {"name": "bottle", "width": 20, "height": 50},
    {"name": "wine glass", "width": 20, "height": 60},
    {"name": "cup", "width": 30, "height": 40},
    {"name": "fork", "width": 10, "height": 40},
    {"name": "knife", "width": 10, "height": 50},
    {"name": "spoon", "width": 15, "height": 40},
    {"name": "bowl", "width": 50, "height": 30},
    {"name": "banana", "width": 40, "height": 20},
    {"name": "apple", "width": 30, "height": 30},
    {"name": "sandwich", "width": 50, "height": 30},
    {"name": "orange", "width": 30, "height": 30},
    {"name": "broccoli", "width": 40, "height": 40},
    {"name": "carrot", "width": 15, "height": 50},
    {"name": "hot dog", "width": 50, "height": 30},
    {"name": "pizza", "width": 60, "height": 60},
    {"name": "donut", "width": 40, "height": 40},
    {"name": "cake", "width": 80, "height": 50},
    {"name": "chair", "width": 100, "height": 120},
    {"name": "couch", "width": 200, "height": 120},
    {"name": "potted plant", "width": 60, "height": 100},
    {"name": "bed", "width": 280, "height": 180},
    {"name": "dining table", "width": 220, "height": 160},
    {"name": "toilet", "width": 120, "height": 150},
    {"name": "tv", "width": 160, "height": 100},
    {"name": "laptop", "width": 100, "height": 80},
    {"name": "mouse", "width": 30, "height": 20},
    {"name": "remote", "width": 30, "height": 70},
    {"name": "keyboard", "width": 120, "height": 40},
    {"name": "cell phone", "width": 40, "height": 80},
    {"name": "microwave", "width": 100, "height": 80},
    {"name": "oven", "width": 150, "height": 120},
    {"name": "toaster", "width": 60, "height": 40},
    {"name": "sink", "width": 100, "height": 80},
    {"name": "refrigerator", "width": 150, "height": 300},
    {"name": "book", "width": 40, "height": 60},
    {"name": "clock", "width": 50, "height": 50},
    {"name": "vase", "width": 30, "height": 60},
    {"name": "scissors", "width": 20, "height": 50},
    {"name": "teddy bear", "width": 80, "height": 100},
    {"name": "hair drier", "width": 60, "height": 60},
    {"name": "toothbrush", "width": 15, "height": 50},
]

HORIZONTAL_DESCRIPTORS: Dict = {
    0: "Left",
    160: "Slightly left",
    320: "Center",
    480: "Slightly right",
    640: "Right",
}
VERTICAL_DESCRIPTORS: Dict = {
    0: "Up",
    120: "Slightly up",
    240: "Center",
    360: "Slightly down",
    480: "Down",
}


class ObjectToText:
    def __init__(self):
        pass

    def get_text(self, class_id, bbox) -> Optional[str]:
        details = self.get_details(class_id, bbox)
        if not details:
            return None
        
        horizontal, vertical = details
        return f'A {class_id} is located {vertical.lower()} and {horizontal.lower()}'

    def get_details(self, name: str, bbox: List[int]) -> Optional[Tuple[str, str]]:        
        min_width = float('inf')
        min_height = float('inf')

        x = bbox[2]
        y = bbox[3]
        width = bbox[2]
        height = bbox[3]

        for object in OBJECT_SIZES:
            if object["name"] != name:
                continue
            
            min_width = object["width"]
            min_height = object["height"]
            break

        if (width <= min_width) or (height <= min_height):
            return None

        return (self.get_descriptor(x, HORIZONTAL_DESCRIPTORS), self.get_descriptor(y, VERTICAL_DESCRIPTORS))

    def get_descriptor(self, value: int, descriptor_map: Dict[int, str]) -> str:
        keys = sorted(descriptor_map.keys())
        for i in range(len(keys)):
            if value <= keys[i]:
                return descriptor_map[keys[i]]
        return descriptor_map[keys[-1]]
