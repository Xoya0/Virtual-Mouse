# Hand Gesture Recognition Virtual Mouse Controller

## Overview

This project implements a hand gesture recognition system that allows users to control a virtual mouse using hand movements. The application utilizes computer vision techniques with the MediaPipe library to recognize various hand gestures, enabling functionalities such as cursor movement, clicking, scrolling, zooming, volume control, and brightness adjustment.

## Features

- **Cursor Movement**: Move the cursor by positioning your hand.
- **Left Click**: Make a fist with your hand.
- **Right Click**: Touch your thumb to your index finger.
- **Double Click**: Quickly touch your thumb to your index finger twice.
- **Scrolling**: Scroll vertically or horizontally by holding your hand flat and moving it.
- **Zoom**: Pinch your thumb and index finger together to zoom in; spread them apart to zoom out.
- **Volume Control**: Raise your hand with palm facing up to increase volume; lower it to decrease volume.
- **Brightness Control**: Move your hand closer to the screen to increase brightness; move it further away to decrease brightness.

## Requirements

- Python 3.x
- OpenCV
- MediaPipe
- PyAutoGUI
- Screen Brightness Control

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Xoya0/Virtual-Mouse.git
   cd virtual_mouse_controller
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   ```bash
   python virtual_mouse_controller/gesture_recognition.py
   ```

2. **Follow the on-screen instructions** to calibrate the system and start using hand gestures to control the virtual mouse.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please fork the repository and submit a pull request.

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Submit a pull request.


## Acknowledgments

- [MediaPipe](https://google.github.io/mediapipe/) for hand tracking and gesture recognition.
- [OpenCV](https://opencv.org/) for computer vision functionalities.
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) for controlling the mouse and keyboard.
- [Screen Brightness Control](https://pypi.org/project/screen-brightness-control/) for adjusting screen brightness.

## Contact

For any inquiries or feedback, please reach out to [dibyanshumohanty4@gmail](dibyanshumohanty4@gmail.com).
