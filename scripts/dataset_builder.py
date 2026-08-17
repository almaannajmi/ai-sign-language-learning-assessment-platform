import os
import csv

from extract_landmarks import extract_landmarks

DATASET_PATH = "datasets/ASL Alphabet Dataset/dataset"
OUTPUT_CSV = "landmarks.csv"

header = []

for i in range(21):
    header.extend([f"x{i}", f"y{i}", f"z{i}"])

header.append("label")

total_images = 0
successful_images = 0
failed_images = 0
failed_files = []

with open(OUTPUT_CSV, mode="w", newline="") as file:

    writer = csv.writer(file)
    writer.writerow(header)
    for class_name in os.listdir(DATASET_PATH):

        class_path = os.path.join(DATASET_PATH, class_name)

        if not os.path.isdir(class_path):
            continue

        print(f"Processing {class_name}...")
        for image_name in os.listdir(class_path):

            total_images += 1

            image_path = os.path.join(class_path, image_name)
            features = extract_landmarks(image_path)
            if features is not None:

                features.append(class_name)

                writer.writerow(features)

                successful_images += 1

            else:

                failed_images += 1

                failed_files.append(image_path)

print("\nDataset Building Completed!")
print(f"CSV saved as: {OUTPUT_CSV}")
print(f"Total images processed: {total_images}")
print(f"Successful detections: {successful_images}")
print(f"Failed detections: {failed_images}")

with open("failed_samples.txt", "w") as file:
    for sample in failed_files:
        file.write(sample + "\n")