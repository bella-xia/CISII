import cv2


def top_hat_transform(gray_img, blender_ratio=0.75):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))  # Adjust kernel size
    top_hat = cv2.morphologyEx(gray_img, cv2.MORPH_TOPHAT, kernel)
    blended = cv2.addWeighted(gray_img, 1 - blender_ratio, top_hat, blender_ratio, 0)
    return blended


def high_pass_filtering(img):
    blurred = cv2.GaussianBlur(img, (21, 21), 0)  # Large kernel
    high_pass = cv2.addWeighted(img, 1.5, blurred, -0.5, 0)
    return high_pass
