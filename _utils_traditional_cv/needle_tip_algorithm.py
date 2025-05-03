import cv2, logging
import numpy as np
from util_modules.needle_reinforcement_module import (
    top_hat_transform,
    high_pass_filtering,
)
from util_modules.visualization_module import (
    visualize_multi,
    visualize_singular,
    visualize_singular_w_lines,
    visualize_singular_w_dot,
)
from util_modules.line_filtering_module import (
    calculate_needle_likelihood,
    filter_by_distance_parallel_threshold,
)
from util_modules.tip_detection_module import get_most_likely_tip
from util_modules.edge_detection_module import (
    edge_detection,
    edge_detection_with_blur_out_red,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def img_preprocess(img_path, top_hat=True, high_pass=False):
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if top_hat:
        gray = top_hat_transform(gray)
    if high_pass:
        gray = high_pass_filtering(gray)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return image, blurred


def straight_line_detection(edges, threshold, minLineLength, maxLineGap):
    return cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180,
        threshold=threshold,
        minLineLength=minLineLength,
        maxLineGap=maxLineGap,
    )


def detect_needle_tip(
    image_path, debug=True, threshold=80, minLineLength=70, maxLineGap=30
):
    image, processed_image = img_preprocess(image_path)
    edges = edge_detection(image, processed_image, min_thres=50, max_thres=200)

    while threshold > 10:
        lines = straight_line_detection(
            edges,
            threshold=threshold,
            minLineLength=minLineLength,
            maxLineGap=maxLineGap,
        )
        if lines is None or len(lines) < 2:
            logger.info(
                f"not capturing enough lines. Decreasing threshold to {threshold - 10}"
            )
            threshold -= 10
            continue
        if debug:
            visualize_multi([image, processed_image, edges], lines)
        for i in range(len(lines) - 1):
            for j in range(i + 1, len(lines)):
                if filter_by_distance_parallel_threshold(lines[i][0], lines[j][0]):
                    logger.info(f"Likely needle tip detected at lines {i} and {j}")
                    needle_tip = get_most_likely_tip(lines[i][0], lines[j][0])
                    logger.info(f"Needle tip at {needle_tip}")
                    visualize_singular_w_dot(image, [lines[i], lines[j]], needle_tip)
                    return
        logger.info(
            f"total line {len(lines)}, No needle tip detected. Decreasing threshold to {threshold - 10}"
        )
        threshold -= 10
    logger.info("fail to detect needle tip.")
    if lines is not None:
        visualize_singular_w_lines(image, lines)


if __name__ == "__main__":
    for i in range(100, 110, 10):
        detect_needle_tip(f"FP_needle_jumped/iOCT_image_000{i}.jpg", debug=False)
