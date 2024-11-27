# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 18:35:23 2024

@author: UOU
"""

import cv2
import numpy as np
import os






# Parameters for drawing
drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial x, y coordinates of the region

rectangles = []  # List to store the rectangles
progress_file = "progress.txt"

# Mouse callback function to draw rectangles
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, rectangles

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y  # Record the starting point

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # Dynamically show the rectangle as the mouse moves
            temp_image = param[0].copy()
            cv2.rectangle(temp_image, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow("Image Segmentation", temp_image)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # Record the rectangle's coordinates
        x1, y1 = min(ix, x), min(iy, y)
        x2, y2 = max(ix, x), max(iy, y)
        rectangles.append((x1, y1, x2 - x1, y2 - y1))  # x, y, width, height

# Function to load the last progress
def load_last_progress():
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            progress = f.read().strip()
            if progress.isdigit():
                return int(progress)
    return 0

# Function to save the current progress
def save_progress(index):
    with open(progress_file, "w") as f:
        f.write(str(index))

# Function to display the image and collect annotations
def segment_images_in_folder(folder_path):
    # Get list of image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()  # Sort files alphabetically for consistent order
    
    if not image_files:
        print("No image files found in the specified folder!")
        return
    
    start_index = load_last_progress()

    for idx, image_file in enumerate(image_files[start_index:], start=start_index):
        image_path = os.path.join(folder_path, image_file)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Could not read image: {image_file}")
            continue

        print(f"Processing: {image_file} ({idx + 1}/{len(image_files)})")
        # Clone of the image for annotation display
        annotated_image = image.copy()
        cv2.namedWindow("Image Segmentation")
        cv2.setMouseCallback("Image Segmentation", draw_rectangle, [annotated_image])
        
        global rectangles
        rectangles = []

        while True:
            # Show the rectangles on the annotated image
            temp_image = annotated_image.copy()
            for rect in rectangles:
                x, y, w, h = rect
                cv2.rectangle(temp_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display the image with annotations
            cv2.imshow("Image Segmentation", temp_image)

            # Key press options
            key = cv2.waitKey(1) & 0xFF
            if key == ord("s"):
                # Save annotations
                annotation_file = os.path.join(folder_path, f"{image_file}_annotations.txt")
                with open(annotation_file, "w") as f:
                    for rect in rectangles:
                        f.write(f"{rect}\n")
                print(f"Annotations saved to {annotation_file}")
            elif key == ord("c"):
                # Clear annotations
                rectangles.clear()
                annotated_image = image.copy()
                print("Annotations cleared")
            elif key == ord("n"):
                annotation_file = os.path.join(folder_path, f"{image_file}_annotations.txt")
                with open(annotation_file, "w") as f:
                    for rect in rectangles:
                        f.write(f"{rect}\n")
                # Move to the next image
                print("Moving to the next image...")
                break
            elif key == ord("q"):
                # Quit the program
                save_progress(idx)
                print(f"Progress saved at image {idx}. Exiting...")
                cv2.destroyAllWindows()
                return
            elif key == ord("z"):
                if rectangles:
                    removed_rect = rectangles.pop()  # Remove the last rectangle
                    print(f"Removed rectangle: {removed_rect}")
                    annotated_image = image.copy()  # Reset the image
                    # Redraw the remaining rectangles
                    for rect in rectangles:
                        x, y, w, h = rect
                        cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                    print("No rectangles to remove!")            

    cv2.destroyAllWindows()


# Example usage
if __name__ == "__main__":
    folder_path = r"C:\Users\ksb80\OneDrive\Desktop\U.U\2024-2\SWDev\Online_Repo2\ImageSet"
    segment_images_in_folder(folder_path)
    print("hi")