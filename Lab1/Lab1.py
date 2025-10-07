#!/usr/bin/env python3
import cv2
import numpy as np

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

if __name__ == "__main__":
    identify_ball_coordinates() 