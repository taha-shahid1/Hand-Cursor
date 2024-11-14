# Hand Cursor
This project enables users to control various computer functions using hand gestures, utilizing computer vision and machine learning. Through specific hand gestures captured by a webcam, users can perform actions like left-click, right-click, volume adjustment, and scrolling.

## Features
Move Cursor: Move your hand with all fingers extended to control the cursor's movement.

Left-Click: Bring your thumb towards your palm with the rest of your fingers extended to perform a left-click.

Right-Click: Bring your ring finger towards your palm with the rest of your fingers extended to perform a right-click.

Volume Adjustment: Extend your thumb and index finger in a "pinch" like gesture. Move your thumb and index finger away or towards each other to change the volume. A volume bar will show up on screen to show the current volume.

Scroll: Extend only your index finger to scroll up, and extend both your index and middle finger to scroll down. 

## Dependencies
opencv-python (for image processing and accessing the webcam)

mediapipe (for hand tracking)

numpy (for numerical operations)

pyautogui (for controlling mouse and system functions)
