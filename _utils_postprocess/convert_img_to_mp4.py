import cv2, glob, argparse, logging

logging.basicConfig(logging.INFO)
logger = logging.getLogger("__convert_img_to_mp4__")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True)
    parser.add_argument("--output", type=str, default="output.mp4")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--img_subfix", type=str, default=".jpg")

    args = parser.parse_args()

    images = sorted(
        glob.glob(f"{args.path}/*{args.img_subfix}"),
        key=lambda x: float(x.split("_")[-1][:-4]),
    )
    if len(images) == 0:
        logger.info(f"unable to find specified images at {args.path}")
        exit(0)

    logger.info(f"found {len(images)} specified images at {args.path}")
    frame = cv2.imread(images[0])
    height, width, layers = frame.shape

    # Define codec and create VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(args.output, fourcc, args.fps, (width, height))

    for img in images:
        frame = cv2.imread(img)
        video.write(frame)

    video.release()
    logger.info(f"Successfully created {args.output}")
    cv2.destroyAllWindows()
