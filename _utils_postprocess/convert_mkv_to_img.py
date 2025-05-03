import cv2, os, logging, argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    parser = argparse.ArgumetParser()
    parser.add_argument("--path", type=str, required=True)
    parser.add_argument("--output", type=str, default="outputs")

    args = parser.parse_args()

    logger.info(f"Converting '{args.path}' to images in '{args.output}'")
    os.makedirs(args.output, exist_ok=True)

    cap = cv2.VideoCapture(args.path)

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Stop if video ends

        # Save frame as an image
        frame_filename = os.path.join(args.path, f"iOCT_image_{frame_count:06d}.jpg")
        cv2.imwrite(frame_filename, frame)

        frame_count += 1

    cap.release()
    print(f"Extracted {frame_count} frames into '{args.output}'")
