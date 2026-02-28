from ultralytics import YOLO
import os
import torch

if __name__ == '__main__':

    # 1. OPTIMIZARE HARDWARE

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    # 2. ALEGERE MODEL
    
    model = YOLO('yolov8m.pt') 

    # 3. CONFIGURARE CALE

    current_folder = os.getcwd() 
    data_path = os.path.join(current_folder, "dataset", "data.yaml")
    
    print(f"START ANTRENAMENT")
    print(f"Config: {data_path}")
    print(f"GPU: {torch.cuda.get_device_name(0)}")

    if not os.path.exists(data_path):
        print("Nu gasesc data.yaml!")
        exit()

    # 4. START ANTRENAMENT (Setari pt RTX 3060 Ti)

    try:
        results = model.train(
            data=data_path, 
            
            # DURATA & RABDARE
            epochs=150,           
            patience=30,          
            
            # MEMORIE & REZOLUTIE
            imgsz=1024,           
            batch=6,              
            
            # OPTIMIZARE VITEZA
            workers=4,            
            cache=False,          
            
            # OPTIMIZARE INVATARE
            optimizer='auto',     
            cos_lr=True,          
            augment=True,         
            
            device=0,             
            name='yolo_train',
        )
    except Exception as e:
        print(f"\nEROARE LA ANTRENARE: {e}")