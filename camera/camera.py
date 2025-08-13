import cv2
import pyautogui
import time

# --- Open Camera ---
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

print("Press 's' to save picture from camera")
print("Press 'c' to take screenshot of laptop screen")
print("Press 'q' to quit")
print("Any key you press will be detected and shown")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    if key != 255:  # 255 means no key was pressed
        print(f"You pressed: '{chr(key)}' (Key code: {key})")

    # Quit
    if key == ord('q'):
        break

    # Save picture from camera
    if key == ord('s'):
        filename = f"captured_{int(time.time())}.png"
        cv2.imwrite(filename, frame)
        print(f"Picture saved as {filename}")

    # Take screenshot of laptop screen
    if key == ord('c'):
        screenshot_filename = f"screenshot_{int(time.time())}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_filename)
        print(f"Screenshot saved as {screenshot_filename}")

# Release camera
cap.release()
cv2.destroyAllWindows()
