import numpy as np
from scipy.spatial.distance import cdist
import logging

logger = logging.getLogger("line_filtering_module")
logging.basicConfig(level=logging.INFO)


def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def is_near(p1, p2, epsilon):
    return distance(p1, p2) < epsilon


def is_near_by_min_distance(line1, line2, dist_threshold):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    points_line1 = np.array([[x1, y1], [x2, y2]])
    points_line2 = np.array([[x3, y3], [x4, y4]])
    distances = cdist(points_line1, points_line2)
    # logger.info(f"min distance: {np.min(distances)}")
    return np.min(distances) < dist_threshold


def near_parallel(line1, line2, max_angle_threshold, min_angle_threshold):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    theta1 = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
    theta2 = np.arctan2(y4 - y3, x4 - x3) * 180 / np.pi

    # Compute the absolute angle difference
    angle_diff = abs(theta1 - theta2)

    # Normalize the angle difference (handle cases > 180 degrees)
    angle_diff = min(angle_diff, 360 - angle_diff)
    logger.info(f"{angle_diff}")
    return angle_diff < max_angle_threshold and angle_diff > min_angle_threshold


def line_angle(p1, p2):
    return np.arctan2(p2[1] - p1[1], p2[0] - p1[0])


def filter_by_distance_parallel_threshold(
    line1, line2, dist_max_threshold=10, max_angle_threshold=5, min_angle_threshold=0.8
):
    return is_near_by_min_distance(line1, line2, dist_max_threshold) and near_parallel(
        line1, line2, max_angle_threshold, min_angle_threshold
    )


def calculate_needle_likelihood(line1, line2, epsilon=1e-2, angle_threshold=np.pi / 6):
    A, B = line1
    C, D = line2

    if is_near(A, C, epsilon):
        meeting_point, outward1, outward2 = A, B, D
    elif is_near(A, D, epsilon):
        meeting_point, outward1, outward2 = A, B, C
    elif is_near(B, C, epsilon):
        meeting_point, outward1, outward2 = B, A, D
    elif is_near(B, D, epsilon):
        meeting_point, outward1, outward2 = B, A, C
    else:
        return 0.0

    # --- Score 1: Intersection Proximity ---
    intersection_score = 1 - (distance(meeting_point, outward1) / epsilon)
    intersection_score = max(0, intersection_score)  # Clamp to [0,1]

    # --- Score 2: Angle Expansion ---
    angle1 = line_angle(meeting_point, outward1)
    angle2 = line_angle(meeting_point, outward2)

    angle_diff = abs(angle1 - angle2)
    if angle_diff > np.pi:
        angle_diff = 2 * np.pi - angle_diff
    angle_score = min(1, angle_diff / angle_threshold)

    # --- Score 3: Length Balance ---
    length1 = distance(meeting_point, outward1)
    length2 = distance(meeting_point, outward2)

    length_ratio = min(length1, length2) / max(length1, length2)
    length_score = length_ratio

    # --- Combine Scores ---
    w1, w2, w3 = 0.4, 0.4, 0.2  # Weights for intersection, angle, and length
    needle_score = w1 * intersection_score + w2 * angle_score + w3 * length_score

    return needle_score
