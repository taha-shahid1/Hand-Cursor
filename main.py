import cv2
import time
import math
import numpy as np
import HandTrackingModule as htm
import pyautogui
import subprocess

# Initialize camera and variables
wCam, hCam = 740, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(maxHands=1, detectionCon=0.85, trackCon=0.8)

# Volume control variables
hmin = 50
hmax = 200
volBar = 400
volPer = 0
vol = 0
color = (0, 0, 0)

tipIds = [4, 8, 12, 16, 20]
mode = ''
active = 0

# Configure pyautogui
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.01  

def putText(mode, loc=(250, 450), color=(0, 255, 255)):
    cv2.putText(img, str(mode), loc, cv2.FONT_HERSHEY_DUPLEX, 3, color, 3)

def set_volume(vol):
    command = f"osascript -e 'set volume output volume {vol}'"
    subprocess.call(command, shell=True)

# Function to determine color based on volume level
def set_volume_color(volume):
    if volume < 30:
        return (0, 255, 0)  # Green for low volume
    elif volume < 70:
        return (0, 215, 255)  # Orange for medium volume
    else:
        return (0, 0, 255)  # Red for high volume

# Variables for smoothing
smoothness_factor = 0.15 
prev_x, prev_y = 0, 0  # Initialize previous cursor position

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip horizontally
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    fingers = []

    if len(lmList) != 0:
        # Check finger positions
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Mode selection
        total_fingers = sum(fingers)
        
        if total_fingers == 0 and active == 0:
            mode = 'N'
        elif (fingers == [0, 1, 0, 0, 0] or fingers == [0, 1, 1, 0, 0]) and active == 0:     # Either only index or middle finger are extended or only index is extended
            mode = 'Scroll'
            active = 1
        elif fingers == [1, 1, 0, 0, 0] and active == 0:                                     # Only index and thumb are extended
            mode = 'Volume'
            active = 1
        elif fingers == [1, 1, 1, 1, 1] and active == 0:                                     # All fingers are extended
            mode = 'Cursor'
            active = 1

    if mode == 'Scroll':
        putText(mode)
        if len(lmList) != 0:
            index_up = lmList[8][2] < lmList[6][2]
            middle_up = lmList[12][2] < lmList[10][2]
            
            if index_up and not middle_up:
                putText('U', (200, 455), (0, 255, 0))
                pyautogui.scroll(1)
            elif index_up and middle_up:
                putText('D', (200, 455), (0, 0, 255))
                pyautogui.scroll(-1)

            if not (index_up or middle_up):
                active = 0
                mode = 'N'

    if mode == 'Volume':
        if len(lmList) != 0:
            if fingers[-1] == 1:
                active = 0
                mode = 'N'
            else:
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                length = math.hypot(x2 - x1, y2 - y1)
                vol = np.interp(length, [hmin, hmax], [0, 100])
                volBar = np.interp(vol, [0, 100], [400, 150])
                volPer = np.interp(vol, [0, 100], [0, 100])

                # Set volume level and color
                set_volume(int(vol))
                color = set_volume_color(volPer)

                cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), color, 3)
                cv2.circle(img, (cx, cy), 8, color, cv2.FILLED)

                # Volume bar and percentage text
                cv2.rectangle(img, (30, 150), (55, 400), (0, 0, 0), 3)
                cv2.rectangle(img, (30, int(volBar)), (55, 400), color, cv2.FILLED)
                cv2.putText(img, f'{int(volPer)}%', (25, 430), cv2.FONT_HERSHEY_DUPLEX, 0.9, color, 3)

    if mode == 'Cursor':
        putText(mode)
        if sum(fingers[1:]) == 0:
            active = 0
            mode = 'N'
        else:
            if len(lmList) != 0:
                screen_width, screen_height = pyautogui.size()
                x1, y1 = lmList[8][1], lmList[8][2]
                
                # Smooth cursor movement with exponential smoothing
                target_x = int(np.interp(x1, [110, 620], [0, screen_width-1]))
                target_y = int(np.interp(y1, [20, 350], [0, screen_height-1]))

                current_x = int(prev_x + smoothness_factor * (target_x - prev_x))
                current_y = int(prev_y + smoothness_factor * (target_y - prev_y))

                pyautogui.moveTo(current_x, current_y)
                prev_x, prev_y = current_x, current_y

                # Check for left-click (thumb brought towards palm)
                if fingers[0] == 0 and fingers[1] == 1:
                    pyautogui.click()
                    time.sleep(0.15)

                # Check for right-click (ring finger brought towards palm)
                elif fingers == [1, 1, 1, 0, 1]:
                    pyautogui.rightClick()
                    time.sleep(0.2)

    # FPS display
    cTime = time.time()
    fps = 1 / ((cTime + 0.01) - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (480, 50), cv2.FONT_ITALIC, 1, (0, 0, 0), 2)
    cv2.imshow('Hand LiveFeed', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
