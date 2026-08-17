from pathlib import Path
import cv2
# Find project root
project_root = Path(__file__).resolve().parent.parent
# Image path
image_path = (
    project_root
    / "datasets"
    / "ASL Alphabet Dataset"
    / "dataset"
    / "A-samples"
    / "0.jpg"
)
if not image_path.exists():
    print("Image not found!")
    exit()
image = cv2.imread(str(image_path))

# Get image dimensions
height, width, channels = image.shape

# Calculate image size
image_size = image.size

print(f"Height   : {height}")
print(f"Width    : {width}")
print(f"Channels : {channels}")
print(f"Image Size : {image_size}")

# Display the image
cv2.imshow("ASL Image", image)

# Wait until a key is pressed
cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()