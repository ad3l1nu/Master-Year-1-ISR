import os
import numpy as np

# Calculam calea de baza relativa la acest fisier
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    # Cai fisiere
    "PATHS": {
        "MODEL": os.path.join(BASE_DIR, 'runs', 'detect', 'yolo_train', 'weights', 'best.pt'),
        "VIDEO": os.path.join(BASE_DIR, 'video.mp4'),
        "OUTPUT": os.path.join(BASE_DIR, 'output_final.mp4')
    },
    
    # Setari vizuale
    "COLORS": {
        "RED": (0, 0, 255),
        "GREEN": (0, 255, 0),
        "YELLOW": (0, 140, 255),
        "BLUE_CYAN": (255, 255, 0),
        "PURPLE": (255, 0, 255),
        "GRAY": (128, 128, 128),
        "WHITE": (255, 255, 255),
        "BLACK": (0, 0, 0)
    },

    # Clase de detectat si setarile lor
    "CLASSES": {
        "car": {
            "conf": 0.75, 
            "label": "Masina", 
            "base_color": (0, 255, 0) 
        },
        "person": {
            "conf": 0.50, 
            "label": "Persoana", 
            "base_color": (255, 255, 0) 
        },
        "traffic_light": {
            "conf": 0.50, 
            "label": "Semafor", 
            "base_color": (128, 128, 128)
        },
        "traffic_sign": {
            "conf": 0.50, 
            "label": "Semn", 
            "base_color": (255, 0, 255)
        }
    },
    
    "HSV_RANGES": {
        "RED_LOW":  (np.array([0, 100, 50]), np.array([8, 255, 255])),
        "RED_HIGH": (np.array([170, 100, 50]), np.array([180, 255, 255])),
        "YELLOW":   (np.array([12, 100, 100]), np.array([35, 255, 255])),
        "GREEN":    (np.array([40, 100, 50]), np.array([90, 255, 255]))
    }
}