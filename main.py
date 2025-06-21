def main() -> None:
    ...

def describe_position(y, x, half_h, half_w):
    center_y = y + half_h
    center_x = x + half_w

    # Horizontal zones
    if center_x < 160:
        horiz = "Left"
    elif center_x < 280:
        horiz = "Slightly left"
    elif center_x <= 360:
        horiz = "Center"
    elif center_x <= 480:
        horiz = "Slightly right"
    else:
        horiz = "Right"

    # Vertical zones
    if center_y < 120:
        vert = "Up"
    elif center_y < 200:
        vert = "Slightly up"
    elif center_y <= 280:
        vert = "Center"
    elif center_y <= 360:
        vert = "Slightly down"  
    else:
        vert = "Down"

    return f"{vert}, {horiz}"

###############################################################

if __name__ == '__main__':
    main()