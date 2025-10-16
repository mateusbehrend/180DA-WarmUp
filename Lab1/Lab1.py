#!/usr/bin/env python3
import cv2
import numpy as np
from sklearn.cluster import KMeans

def identify_ball_coordinates():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    while True:
        ret, frame = cap.read()
        if ret:

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            cv2.imshow('HSV Frame', hsv)

            lower_yellow_green = np.array([25, 100, 100])
            upper_yellow_green = np.array([75, 255, 255])
            mask = cv2.inRange(hsv, lower_yellow_green, upper_yellow_green)
            cv2.imshow('Mask', mask)

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0:
                largest_contour = max(contours, key=cv2.contourArea)

                ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
                # Make sure that the detected radius is large enough and the object we are looing for
                if radius > 10:
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                    print(f"Ball detected at coordinates: X={x}, Y={y}, Radius={radius}")

            cv2.imshow('Video Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break 
    cap.release()
    cv2.destroyAllWindows()


# Task 3
def identify_post_it():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    while True:
        ret, frame = cap.read()
        if ret:
            # Question: RGB or HSV? HSV is typically better for color detection
            # RGB is more intuitive but sensitive to brightness and lighting changes
            # HSV separates color information (hue) from intensity (value), making it more robust
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            cv2.imshow('HSV Frame', hsv)

            # Define the HSV range for pink
            lower_red1 = np.array([0, 130, 100])
            lower_red2 = np.array([160, 130, 100])
            upper_red1 = np.array([10, 255, 255])
            upper_red2 = np.array([179, 255, 255])
            
            # Create a mask for each range
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

            # Question:
            # My threshold range to capture the values is Hue 0 - 10 and 160 -179
            # Saturation 130 - 255
            # Value 100 - 255

            # Combine the two masks
            mask = cv2.add(mask1, mask2)
            cv2.imshow('Mask', mask)

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Question
            # I turned off the lights in the room, however the light from my monitor plus laptop were enough to illuminate the pink notepad 
            # This made the detection much better 
            # However, when moved much further away, the detection was lost and much harder to achieve. 
            # I think this is because the color is less saturated and the camera has a harder time picking it up.

            # Question 
            # Color picker tool displayed on phone was able to be captured by the camera very well especially with the brightness raised
            # However, when a bit darker the color was not picked up as well, but was suprisingly still detected.
            # When it was brightest it was able to be detected very well.

            if len(contours) > 0:
                largest_contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(largest_contour) > 500:
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow('Video Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break 
    cap.release()
    cv2.destroyAllWindows()

def find_dominant_color(image, k=3):
    """
    Finds the k dominant colors in an image and returns the most dominant one.
    """
    # Reshape the image to be a list of pixels (n_pixels, 3 channels)
    pixels = image.reshape((-1, 3))
    pixels = np.float32(pixels)

    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=k, n_init='auto', random_state=0)
    kmeans.fit(pixels)

    # Find the most frequent cluster
    unique_labels, counts = np.unique(kmeans.labels_, return_counts=True)
    dominant_cluster_index = unique_labels[np.argmax(counts)]
    dominant_color = kmeans.cluster_centers_[dominant_cluster_index]
    
    return dominant_color.astype(np.uint8)


# Task 3 determining the dominant color in a designated rectangle 
# The phone seems to a bit more resistance to brightness becuase the physical object reflects light and needs the presence of a light source 
# If the light of my laptop wasn't so strong it would be very hard to capture the color of the physical object
# In theory, and in practice the phone portraying the light would be more effective.
def dominant_color_detector():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        #  Define a central rectangle (Region of Interest - ROI)
        h, w, _ = frame.shape
        roi_size = 400
        x1 = (w - roi_size) // 2
        y1 = (h - roi_size) // 2
        x2 = x1 + roi_size
        y2 = y1 + roi_size

        roi = frame[y1:y2, x1:x2]

        if roi.size > 0:
            # Find the dominant color in the ROI
            dominant_color = find_dominant_color(roi, k=4) # Using 4 clusters
            
            # Create a color swatch to display the result
            swatch = np.zeros((100, frame.shape[1], 3), dtype=np.uint8)
            swatch[:] = dominant_color 

            # Draw the ROI rectangle on the main video feed for clarity
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            cv2.imshow('Dominant Color', swatch)

        cv2.imshow('Video Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    dominant_color_detector()