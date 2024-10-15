import cv2
import mediapipe as mp
import time
import pyautogui
import screen_brightness_control as sbc 

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Calibration factor for cursor speed
calibration_factor = 1.0

def calibrate():
    global calibration_factor
    print("Calibration started. Move your hand to the desired position.")
    time.sleep(5)  # Allow user to position their hand
    calibration_factor = 1.5  # Example value; implement a more sophisticated method if needed

def move_cursor(hand_landmarks):
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    screen_width, screen_height = pyautogui.size()
    cursor_x = int(wrist.x * screen_width * calibration_factor)
    cursor_y = int(wrist.y * screen_height * calibration_factor)
    pyautogui.moveTo(cursor_x, cursor_y)

def is_fist(hand_landmarks):
    return all(hand_landmarks.landmark[i].y > hand_landmarks.landmark[i - 1].y for i in range(1, 5))

def is_thumb_index_touch(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    distance = ((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) ** 0.5
    return distance < 0.05  # Adjust threshold as needed

def is_hand_flat(hand_landmarks):
    return all(hand_landmarks.landmark[i].y < hand_landmarks.landmark[i - 1].y for i in range(1, 5))

def is_hand_raised(hand_landmarks):
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    return wrist.y < index_finger_tip.y

def is_hand_lowered(hand_landmarks):
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    return wrist.y > index_finger_tip.y

def adjust_volume(increase=True):
    if increase:
        print("Volume Increased")
        # Implement actual volume control logic here
    else:
        print("Volume Decreased")

def adjust_brightness(increase=True):
    current_brightness = sbc.get_brightness()[0]  # Get the first brightness value
    if increase:
        sbc.set_brightness(min(current_brightness + 10, 100))  # Increase brightness
        print("Brightness Increased")
    else:
        sbc.set_brightness(max(current_brightness - 10, 0))  # Decrease brightness
        print("Brightness Decreased")

def is_scrolling(hand_landmarks):
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    return index_finger_tip.y < thumb_tip.y, index_finger_tip.y > thumb_tip.y  # Returns (scroll up, scroll down)

def is_pinch_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    distance = ((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) ** 0.5
    return distance < 0.05  # Adjust threshold as needed

def is_spreading_fingers(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    distance = ((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) ** 0.5
    return distance > 0.1  # Adjust threshold as needed for zoom out

# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Move the cursor using wrist position
            move_cursor(hand_landmarks)

            # Recognize gestures and provide feedback
            if is_fist(hand_landmarks):
                cv2.putText(frame, "Left Click", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                continue  # Skip further checks if left click is detected
            elif is_thumb_index_touch(hand_landmarks):
                cv2.putText(frame, "Right Click", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                continue  # Skip further checks if right click is detected
            elif is_hand_flat(hand_landmarks):
                scroll_up, scroll_down = is_scrolling(hand_landmarks)
                if scroll_up:
                    cv2.putText(frame, "Scrolling Up", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    pyautogui.scroll(10)  # Scroll up
                elif scroll_down:
                    cv2.putText(frame, "Scrolling Down", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    pyautogui.scroll(-10)  # Scroll down
                continue  # Skip further checks if scrolling is detected
            elif is_hand_raised(hand_landmarks):
                adjust_volume(increase=True)
                cv2.putText(frame, "Volume Up", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                continue  # Skip further checks if volume up is detected
            elif is_hand_lowered(hand_landmarks):
                adjust_volume(increase=False)
                cv2.putText(frame, "Volume Down", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                continue  # Skip further checks if volume down is detected
            elif is_pinch_gesture(hand_landmarks):
                cv2.putText(frame, "Zoom In", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                continue  # Skip further checks if zoom in is detected
            elif is_spreading_fingers(hand_landmarks):
                cv2.putText(frame, "Zoom Out", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                continue  # Skip further checks if zoom out is detected

            # Brightness control based on distance from the camera
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            if wrist.z < 0:
                adjust_brightness(increase=True)
            else:
                adjust_brightness(increase=False)

    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()