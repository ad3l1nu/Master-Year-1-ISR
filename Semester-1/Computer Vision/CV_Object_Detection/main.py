import cv2
import os
from ultralytics import YOLO

#IMPORTURI LOCALE
from config import CONFIG
from logic import analyze_traffic_light, analyze_traffic_sign
from visualization import draw_detection_box

print("--- START SYSTEM ---")

# 1. Setup
if not os.path.exists(CONFIG["PATHS"]["MODEL"]):
    print("EROARE: Lipseste modelul!")
    exit()

model = YOLO(CONFIG["PATHS"]["MODEL"])
cap = cv2.VideoCapture(CONFIG["PATHS"]["VIDEO"])
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(CONFIG["PATHS"]["OUTPUT"], cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

try:
    while True:
        ret, frame = cap.read()
        if not ret: break

        results = model(frame, verbose=False)

        for r in results:
            for box in r.boxes:
                # Date brute
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                name = model.names[cls_id]

                # Filtrare
                if name not in CONFIG["CLASSES"]: continue
                settings = CONFIG["CLASSES"][name]
                if conf < settings["conf"]: continue

                # Crop
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                crop = frame[max(0,y1):min(height,y2), max(0,x1):min(width,x2)]

                # Logica (folosim functiile importate din logic.py)
                color = settings["base_color"]
                label = settings["label"]

                if name == 'traffic_light':
                    color, label = analyze_traffic_light(crop)
                elif name == 'traffic_sign':
                    color, label = analyze_traffic_sign(crop)

                # Formatare text cu procent
                full_label = f"{label} {int(conf * 100)}%"

                # Desenare (folosim functia importata din visualization.py)
                draw_detection_box(frame, (x1, y1, x2, y2), color, full_label)

        # Afisare
        cv2.imshow('Final', cv2.resize(frame, (1280, 720)))
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Eroare: {e}")
finally:
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Finalizat.")