from typing import Dict, Tuple, Optional

CONFIDENCE_THRESHOLD: float = 0.5

OBJECT_SIZES = {
    0: {"name": "person", "width": 60, "height": 160},
    1: {"name": "bicycle", "width": 150, "height": 100},
    2: {"name": "car", "width": 180, "height": 120},
    3: {"name": "motorcycle", "width": 160, "height": 100},
    4: {"name": "airplane", "width": 300, "height": 150},
    5: {"name": "bus", "width": 300, "height": 200},
    6: {"name": "train", "width": 400, "height": 150},
    7: {"name": "truck", "width": 250, "height": 150},
    8: {"name": "boat", "width": 140, "height": 100},
    9: {"name": "traffic light", "width": 30, "height": 90},
    10: {"name": "fire hydrant", "width": 40, "height": 70},
    11: {"name": "stop sign", "width": 60, "height": 60},
    12: {"name": "parking meter", "width": 30, "height": 100},
    13: {"name": "bench", "width": 120, "height": 60},
    14: {"name": "bird", "width": 60, "height": 40},
    15: {"name": "cat", "width": 80, "height": 60},
    16: {"name": "dog", "width": 100, "height": 80},
    17: {"name": "horse", "width": 160, "height": 120},
    18: {"name": "sheep", "width": 140, "height": 100},
    19: {"name": "cow", "width": 180, "height": 120},
    20: {"name": "elephant", "width": 220, "height": 160},
    21: {"name": "bear", "width": 200, "height": 150},
    22: {"name": "zebra", "width": 200, "height": 140},
    23: {"name": "giraffe", "width": 150, "height": 300},
    24: {"name": "backpack", "width": 50, "height": 70},
    25: {"name": "umbrella", "width": 60, "height": 80},
    26: {"name": "handbag", "width": 50, "height": 60},
    27: {"name": "tie", "width": 20, "height": 60},
    28: {"name": "suitcase", "width": 70, "height": 90},
    29: {"name": "frisbee", "width": 60, "height": 60},
    30: {"name": "skis", "width": 120, "height": 30},
    31: {"name": "snowboard", "width": 100, "height": 40},
    32: {"name": "sports ball", "width": 50, "height": 50},
    33: {"name": "kite", "width": 100, "height": 100},
    34: {"name": "baseball bat", "width": 20, "height": 80},
    35: {"name": "baseball glove", "width": 50, "height": 50},
    36: {"name": "skateboard", "width": 100, "height": 40},
    37: {"name": "surfboard", "width": 120, "height": 40},
    38: {"name": "tennis racket", "width": 50, "height": 80},
    39: {"name": "bottle", "width": 20, "height": 50},
    40: {"name": "wine glass", "width": 20, "height": 60},
    41: {"name": "cup", "width": 30, "height": 40},
    42: {"name": "fork", "width": 10, "height": 40},
    43: {"name": "knife", "width": 10, "height": 50},
    44: {"name": "spoon", "width": 15, "height": 40},
    45: {"name": "bowl", "width": 50, "height": 30},
    46: {"name": "banana", "width": 40, "height": 20},
    47: {"name": "apple", "width": 30, "height": 30},
    48: {"name": "sandwich", "width": 50, "height": 30},
    49: {"name": "orange", "width": 30, "height": 30},
    50: {"name": "broccoli", "width": 40, "height": 40},
    51: {"name": "carrot", "width": 15, "height": 50},
    52: {"name": "hot dog", "width": 50, "height": 30},
    53: {"name": "pizza", "width": 60, "height": 60},
    54: {"name": "donut", "width": 40, "height": 40},
    55: {"name": "cake", "width": 80, "height": 50},
    56: {"name": "chair", "width": 100, "height": 120},
    57: {"name": "couch", "width": 200, "height": 120},
    58: {"name": "potted plant", "width": 60, "height": 100},
    59: {"name": "bed", "width": 280, "height": 180},
    60: {"name": "dining table", "width": 220, "height": 160},
    61: {"name": "toilet", "width": 120, "height": 150},
    62: {"name": "tv", "width": 160, "height": 100},
    63: {"name": "laptop", "width": 100, "height": 80},
    64: {"name": "mouse", "width": 30, "height": 20},
    65: {"name": "remote", "width": 30, "height": 70},
    66: {"name": "keyboard", "width": 120, "height": 40},
    67: {"name": "cell phone", "width": 40, "height": 80},
    68: {"name": "microwave", "width": 100, "height": 80},
    69: {"name": "oven", "width": 150, "height": 120},
    70: {"name": "toaster", "width": 60, "height": 40},
    71: {"name": "sink", "width": 100, "height": 80},
    72: {"name": "refrigerator", "width": 150, "height": 300},
    73: {"name": "book", "width": 40, "height": 60},
    74: {"name": "clock", "width": 50, "height": 50},
    75: {"name": "vase", "width": 30, "height": 60},
    76: {"name": "scissors", "width": 20, "height": 50},
    77: {"name": "teddy bear", "width": 80, "height": 100},
    78: {"name": "hair drier", "width": 60, "height": 60},
    79: {"name": "toothbrush", "width": 15, "height": 50}
}

HORIZONTAL_DESCRIPTORS: Dict = {
    0: "Left",
    160: "Slightly left",
    320: "Center",
    480: "Slightly right",
    640: "Right"

}
VERTICAL_DESCRIPTORS: Dict = {
    0: "Up",
    120: "Slightly up", 
    240: "Center",
    360: "Slightly down",
    480: "Down"
}

class ObjectToText:
    def __init__(self):
        self._last_size = {"w": 0, "h": 0}

    def classify(self, x: int, y: int) -> Tuple[str, str]:
        return self._get_descriptor(x, HORIZONTAL_DESCRIPTORS), self._get_descriptor(y, VERTICAL_DESCRIPTORS)

    def _get_descriptor(value: int, descriptor_map: Dict[int, str]) -> str:
        keys = sorted(descriptor_map.keys())
        for i in range(len(keys)):
            if value <= keys[i]:
                return descriptor_map[keys[i]]
        return descriptor_map[keys[-1]]

    def detect(
        self,
        name: str,
        x: int,
        y: int,
        w: int,
        h: int,
        confidence: float
    ) -> Optional[str]:
        if confidence < CONFIDENCE_THRESHOLD:
            return None
        
        if w <= self._last_size["w"] or h <= self._last_size["h"]: 
            return ""
        
        self._last_size.update({"w": w, "h": h})
        horiz, vert = self.classify(x, y)
        return f"The {name} is located {vert.lower()}, {horiz.lower()}"