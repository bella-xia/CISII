import cv2
import numpy as np


def filter_contour_by_area(edges, min_area=100):
    # Load the image and apply Canny edge detection
    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    filtered_contours = np.zeros_like(edges)
    for contour in contours:
        if cv2.contourArea(contour) > min_area:
            cv2.drawContours(
                filtered_contours, [contour], -1, (255), thickness=cv2.FILLED
            )

    return filtered_contours


def filter_based_on_perimeter(edges, min_perimeter=50):
    filtered_contours = np.zeros_like(edges)
    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    for contour in contours:
        if cv2.arcLength(contour, closed=True) > min_perimeter:
            cv2.drawContours(
                filtered_contours, [contour], -1, (255), thickness=cv2.FILLED
            )
    return filtered_contours
