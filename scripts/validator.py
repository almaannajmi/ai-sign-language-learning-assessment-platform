import os
import json

DATASET_PATH = "datasets/ASL Alphabet Dataset/dataset"
CSV_FILE = "landmarks.csv"
FAILED_FILE = "failed_samples.txt"
REPORT_FILE = "dataset_report.json"

# Count total images in dataset
total_images = 0
corrupted_images = 0

for class_name in os.listdir(DATASET_PATH):
    class_path = os.path.join(DATASET_PATH, class_name)

    if not os.path.isdir(class_path):
        continue

    for image_name in os.listdir(class_path):
        image_path = os.path.join(class_path, image_name)

        if os.path.isfile(image_path):
            total_images += 1
        else:
            corrupted_images += 1

# Count successful landmark detections
with open(CSV_FILE, "r") as file:
    successful_images = sum(1 for _ in file) - 1  # Exclude header

# Count failed landmark detections
with open(FAILED_FILE, "r") as file:
    failed_images = len(file.readlines())

# Calculate success percentage
success_percentage = (
    (successful_images / total_images) * 100
    if total_images > 0
    else 0
)

# Create report dictionary
report = {
    "total_images_processed": total_images,
    "successful_landmark_detections": successful_images,
    "failed_landmark_detections": failed_images,
    "corrupted_or_unreadable_images": corrupted_images,
    "success_percentage": round(success_percentage, 2)
}

# Save report
with open(REPORT_FILE, "w") as file:
    json.dump(report, file, indent=4)

# Print summary
print("\n========== DATASET VALIDATION REPORT ==========")
print(f"Total Images Processed      : {total_images}")
print(f"Successful Detections       : {successful_images}")
print(f"Failed Detections           : {failed_images}")
print(f"Corrupted Images            : {corrupted_images}")
print(f"Success Percentage          : {success_percentage:.2f}%")
print(f"\nReport saved as {REPORT_FILE}")