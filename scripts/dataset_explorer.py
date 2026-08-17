from pathlib import Path
import json
# Find the project root directory
project_root = Path(__file__).resolve().parent.parent

# Dataset folder
datasets_folder = project_root / "datasets"
# Find the ASL dataset folder
asl_dataset = datasets_folder / "ASL Alphabet Dataset" / "dataset"
if not asl_dataset.exists():
    print("ASL dataset not found!")
    exit()

# Detect all class folders
class_folders = sorted(
    [folder for folder in asl_dataset.iterdir() if folder.is_dir()]
)

print("Class folders found:")

for folder in class_folders:
    print(folder.name)

# Count images in each class
total_images = 0

for folder in class_folders:
    image_count = len([
        file for file in folder.iterdir()
        if file.is_file()
    ])

    total_images += image_count
    print(f"{folder.name}: {image_count} images")

print("\n--------------------------------")
print(f"Total Classes: {len(class_folders)}")
print(f"Total Images: {total_images}")

# ---------------- WLASL Dataset ----------------

wlasl_folder = datasets_folder / "WLASL"
annotation_file = wlasl_folder / "WLASL_v0.3.json"

if not annotation_file.exists():
    print("\nWLASL annotation file not found!")
    exit()

print("\nWLASL annotation file found:")
print(annotation_file)

# Read the annotation file
with open(annotation_file, "r", encoding="utf-8") as file:
    wlasl_data = json.load(file)

# Count unique signs
unique_signs = len(wlasl_data)

print(f"\nUnique Signs: {unique_signs}")
print("\nFirst 5 Sample Entries:")

for entry in wlasl_data[:5]:
    print(entry)