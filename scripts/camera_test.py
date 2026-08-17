import cv2

# Open the default webcam
camera = cv2.VideoCapture(0)

fps = camera.get(cv2.CAP_PROP_FPS)
print(f"Current FPS: {fps}")

# Check if webcam opened successfully
if not camera.isOpened():
    print("Cannot access webcam!")
    exit()

print("Press Q to quit.")

while True:
    # Capture one frame
    success, frame = camera.read()

    if not success:
        print("Failed to capture frame.")
        break

    # Display the live camera feed
    cv2.imshow("Webcam Verification", frame)

    # Exit when Q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam
camera.release()

# Close all OpenCV windows
cv2.destroyAllWindows()