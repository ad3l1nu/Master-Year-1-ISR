import cv2
from config import CONFIG

def get_contrast_text_color(bg_color):
    lum = bg_color[0] + bg_color[1] + bg_color[2]
    return CONFIG["COLORS"]["WHITE"] if lum < 300 else CONFIG["COLORS"]["BLACK"]

def draw_detection_box(frame, box_coords, color, text):
    """Deseneaza chenarul si eticheta."""
    x1, y1, x2, y2 = box_coords
    
    # Chenar
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    # Fundal Text
    (w_text, h_text), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    cv2.rectangle(frame, (x1, y1 - 25), (x1 + w_text, y1), color, -1)

    # Text
    txt_col = get_contrast_text_color(color)
    cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, txt_col, 2)