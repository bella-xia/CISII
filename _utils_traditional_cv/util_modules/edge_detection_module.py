import cv2, numpy


def edge_detection(image, processed_img, min_thres=150, max_thres=300):
    edges = cv2.Canny(processed_img, min_thres, max_thres)
    return edges


def edge_detection_with_filter_by_saturation(image, gray, min_thres=150, max_thres=300):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1]
    _, sat_mask = cv2.threshold(saturation, 50, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(gray, min_thres, max_thres)
    edges = cv2.bitwise_and(edges, edges, mask=sat_mask)
    return edges


def edge_detection_with_blur_out_red(image, gray, min_thres=150, max_thres=300):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define mask to filter out red surroundings
    lower_red1 = numpy.array([0, 120, 70])
    upper_red1 = numpy.array([10, 255, 255])
    lower_red2 = numpy.array([170, 120, 70])
    upper_red2 = numpy.array([180, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = mask_red1 | mask_red2

    # Invert the mask to keep non-red areas (needle)
    mask_needle = cv2.bitwise_not(mask_red)

    # Convert image to grayscale and apply the mask
    mean_gray = numpy.mean(gray[mask_needle > 0])
    gray[mask_red > 0] = mean_gray

    edges = cv2.Canny(gray, min_thres, max_thres)

    return edges
