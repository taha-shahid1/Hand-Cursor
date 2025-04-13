# Hand Cursor
This project enables users to control various computer functions using hand gestures, utilizing computer vision and machine learning. Through specific hand gestures captured by a webcam, users can perform actions like left-click, right-click, volume adjustment, and scrolling.

## Features

- **Move Cursor**: Control the mouse by simply moving your hand with all fingers extended.
- **Left Click**: Fold your thumb toward your palm while keeping the other fingers extended.
- **Right Click**: Fold your ring finger toward your palm while the rest stay extended.
- **Volume Control**: Use a pinch gesture (thumb + index finger) and adjust the distance to control system volume. A volume bar will appear for feedback.
- **Scroll**: 
  - Scroll up: Extend only your index finger.
  - Scroll down: Extend both your index and middle fingers.

## Dependencies

All required packages are listed in [`requirements.txt`](./requirements.txt).  
Make sure to use **Python 3.7–3.10** — `mediapipe` is not supported on Python 3.11+.

To install everything:

```bash
pip install -r requirements.txt