# Master Year 1 - ISR

Repository containing projects and assignments for the first year of Master's degree in Intelligent Systems and Robotics.

## Semester 1

### 1. Architectures for Parallel Computing
Parallel computing implementations and algorithms:
- **BroadcastFIR.py** - Broadcast-based Finite Impulse Response filter
- **RipplingFIR.py** - Rippling Finite Impulse Response filter
- **CA.py** - Cellular Automaton simulations
- **GoL.py** - Game of Life implementation
- **M x M.py** - Matrix operations and computations

### 2. Computer Vision
YOLO-based object detection project with custom dataset training:
- **Dataset**: Custom annotated dataset with train/valid/test splits
- **Models**: YOLOv8m and YOLOv11n pre-trained weights
- **Training**: Custom model training with results and weights in `runs/detect/yolo_train/`
- **Key Files**:
  - `main.py` - Main execution script
  - `train.py` - Model training pipeline
  - `logic.py` - Core detection logic
  - `visualization.py` - Results visualization
  - `config.py` - Configuration settings
  - `requirements.txt` - Dependencies

### 3. Distributed Systems

#### AI Agent Movies
Multi-agent system for movie recommendations using Firebase and Gemini API:
- **Firebase Integration** - Cloud database and authentication
- **Gemini Service** - AI-powered movie recommendations
- **Movie Service** - Movie data management
- **GUI** - User interface for agent interactions
- **Features**: Real-time agent communication, movie recommendations

#### Chat Client-Server
Network communication implementation with echo protocol:
- **echo_server_multi.py** - Multi-client server implementation
- **echo_client_improved.py** - Enhanced client with improvements
- **echo_client_multi.py** - Multi-threaded client
- **echo_protocol.py** - Protocol definitions

## Semester 2
(In progress)