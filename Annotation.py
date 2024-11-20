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

# 기존 코드
# # List to store segmentation points
# annotations = []

# # Mouse callback function to draw contours
# def draw_contour(event, x, y, flags, param):
#     global ix, iy, drawing

#     if event == cv2.EVENT_LBUTTONDOWN:
#         drawing = True
#         ix, iy = x, y
#         annotations.append([(x, y)])  # Start a new contour

#     elif event == cv2.EVENT_MOUSEMOVE:
#         if drawing:
#             # Add points to the current contour
#             annotations[-1].append((x, y))

#     elif event == cv2.EVENT_LBUTTONUP:
#         drawing = False
#         # Close the contour by connecting the last point to the first
#         annotations[-1].append((x, y))

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

# Function to display the image and collect annotations
# 기존 코드 2
'''
def segment_image(image_path):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found!")
        return

    # Create a clone of the image for annotation display
    annotated_image = image.copy()
    cv2.namedWindow("Image Segmentation")
    # cv2.setMouseCallback("Image Segmentation", draw_contour)
    cv2.setMouseCallback("Image Segmentation", draw_rectangle, [annotated_image])

    while True:
        # Show the annotations on the cloned image
        temp_image = annotated_image.copy()
        # for contour in annotations:
        #     points = np.array(contour, dtype=np.int32)
        #     cv2.polylines(temp_image, [points], isClosed=True, color=(0, 255, 0), thickness=2)
        for rect in rectangles:
            x, y, w, h = rect
            cv2.rectangle(temp_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the image with annotations
        cv2.imshow("Image Segmentation", temp_image)
        
        # Press 's' to save annotations, 'c' to clear, and 'q' to quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            # Save annotations
            with open("annotations.txt", "w") as f:
                # for contour in annotations:
                    # f.write(str(contour) + "\n")
                for rect in rectangles :
                    f.write(f"{rect}\n")
            print("Annotations saved to annotations.txt")
        elif key == ord("c"):
            # Clear annotations
            # annotations.clear()
            rectangles.clear()
            annotated_image = image.copy()
            print("Annotations cleared")
        elif key == ord("q"):
            break

    cv2.destroyAllWindows()
'''


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

def segment_images_in_folder(folder_path):
    # Get list of image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()  # Sort files alphabetically for consistent order
    
    if not image_files:
        print("No image files found in the specified folder!")
        return
    
    start_index = load_last_progress()

    for idx, image_file in enumerate(image_files):
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

    cv2.destroyAllWindows()


# Example usage
if __name__ == "__main__":
    # PathNames = r"C:\Users\ksb80\OneDrive\Desktop\U.U\2024-2\SWDev\Online_Repo2\ImageSet"
    # segment_image(PathNames + "//000000079031.jpg")
    folder_path = r"C:\Users\ksb80\OneDrive\Desktop\U.U\2024-2\SWDev\Online_Repo2\ImageSet"
    segment_images_in_folder(folder_path)
