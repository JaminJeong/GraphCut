import cv2

color_string_map = {
    'red': [255, 0, 0],
    'blue': [0, 255, 0],
    'green': [0, 0, 255],
    'black': [0, 0, 0],
    'white': [255, 255, 255],
    'yellow': [0, 255, 255],
}

def draw_FiilText(draw_img,
                  text,
                  p1_x, p1_y,
                  color_font=color_string_map['yellow'],
                  color_fill=color_string_map['black'],
                  font=cv2.FONT_HERSHEY_SIMPLEX,
                  font_scale=1,
                  thickness=2):

    size = cv2.getTextSize(text, font, font_scale, thickness)
    cv2.rectangle(draw_img, (p1_x, p1_y - 10), (p1_x + size[0][0], p1_y - 10 - size[0][1]), color_fill, cv2.FILLED)
    cv2.putText(draw_img, text, (p1_x, p1_y - 10), font, font_scale, color_font, thickness, cv2.LINE_AA)

