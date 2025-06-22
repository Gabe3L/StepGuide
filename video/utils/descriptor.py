from typing import Dict

#####################################################################

horizontal_descriptors: Dict = {
    0: "Left",
    160: "Slightly left",
    320: "Center",
    480: "Slightly right",
    640: "Right"

}
vertical_descriptors: Dict = {
    0: "Up",
    120: "Slightly up", 
    240: "Center",
    360: "Slightly down",
    480: "Down"

}

#####################################################################

def get_descriptor(value: int, descriptor_map: Dict[int, str]) -> str:
    keys = sorted(descriptor_map.keys())
    for i in range(len(keys)):
        if value <= keys[i]:
            return descriptor_map[keys[i]]
    return descriptor_map[keys[-1]]

#####################################################################

def main():
    x = 440
    y = 70

    horizontal = get_descriptor(x, horizontal_descriptors)
    vertical = get_descriptor(y, vertical_descriptors)

    print(f"Horizontal: {horizontal}, Vertical: {vertical}")

#####################################################################

if __name__ == '__main__':
    main()