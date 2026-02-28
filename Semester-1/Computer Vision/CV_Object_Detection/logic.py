import cv2
import numpy as np
from config import CONFIG

def analyze_traffic_light(img_crop):
    """Detecteaza culoarea semaforului folosind HSV si procentaje."""
    if img_crop is None or img_crop.size == 0:
        return CONFIG["COLORS"]["GRAY"], "UNKNOWN"

    # Calculam numarul total de pixeli din crop (Inaltime x Latime)
    total_pixels = img_crop.shape[0] * img_crop.shape[1]
    
    # Evitam impartirea la zero (just in case)
    if total_pixels == 0:
        return CONFIG["COLORS"]["GRAY"], "UNKNOWN"

    hsv = cv2.cvtColor(img_crop, cv2.COLOR_BGR2HSV)
    ranges = CONFIG["HSV_RANGES"]

    mask_red = cv2.add(
        cv2.inRange(hsv, *ranges["RED_LOW"]),
        cv2.inRange(hsv, *ranges["RED_HIGH"])
    )
    mask_yellow = cv2.inRange(hsv, *ranges["YELLOW"])
    mask_green = cv2.inRange(hsv, *ranges["GREEN"])

    r = cv2.countNonZero(mask_red)
    y = cv2.countNonZero(mask_yellow)
    g = cv2.countNonZero(mask_green)

    m = max(r, y, g)
    
    # Calculam procentul culorii dominante
    dominance_ratio = m / total_pixels

    if dominance_ratio < 0.05: 
        return CONFIG["COLORS"]["GRAY"], "OFF"

    if m == r: return CONFIG["COLORS"]["RED"], "ROSU"
    elif m == g: return CONFIG["COLORS"]["GREEN"], "VERDE"
    elif m == y: return CONFIG["COLORS"]["YELLOW"], "GALBEN"
    
    return CONFIG["COLORS"]["GRAY"], "UNKNOWN"

def analyze_traffic_sign(img_crop):
    """Detecteaza daca semnul este de pericol (Rosu) bazat pe densitatea culorii."""
    if img_crop is None or img_crop.size == 0:
        return CONFIG["COLORS"]["PURPLE"], "Semn"

    total_pixels = img_crop.shape[0] * img_crop.shape[1]
    if total_pixels == 0:
        return CONFIG["COLORS"]["PURPLE"], "Semn"

    hsv = cv2.cvtColor(img_crop, cv2.COLOR_BGR2HSV)
    
    # Interval 1: Rosu spre portocaliu (0 - 10)
    # Am scazut Saturatia (S) la 70 ca sa prinda si semne putin mai sterse
    mask1 = cv2.inRange(hsv, np.array([0, 70, 50]), np.array([10, 255, 255]))
    
    # Interval 2: Rosu spre violet (170 - 180) - Aici sunt multe semne STOP
    mask2 = cv2.inRange(hsv, np.array([170, 70, 50]), np.array([180, 255, 255]))
    
    mask_danger = cv2.add(mask1, mask2)
    
    red_count = cv2.countNonZero(mask_danger)
    red_ratio = red_count / total_pixels

    if red_ratio > 0.10:
        return CONFIG["COLORS"]["RED"], "Semn (!)"
    
    return CONFIG["COLORS"]["PURPLE"], "Semn"