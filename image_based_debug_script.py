import logging, os, cv2
from image_based_util_unet import ImageProcessor
from tqdm import tqdm

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="logger.out",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    MODEL_PATH = "model_weights/unet-2.3k-augmented-wbase-wspaceaug.pth"
    IMG_PATH = "C:/Users/zhiha/OneDrive/Desktop/Chicken_Embryo_Experiment_Puncture_Detection/mojtaba_test_1/_recordings/egg_01/01_FP"

    image_dir = [
        img
        for img in os.listdir(IMG_PATH)
        if img.endswith(".jpg") and img.startswith("iOCT")
    ]
    filtered_img_dir = []
    for img in image_dir:
        try:
            ts = float(img.split("_")[-1].split(".jpg")[0])
            filtered_img_dir.append(img)
        except:
            continue
    sorted_img_dir = sorted(
        filtered_img_dir, key=lambda x: float(x.split("_")[-1].split(".jpg")[0])
    )
    print(f"first image {sorted_img_dir[0]} -- last image {sorted_img_dir[-1]}")
    print(f"there are a total of {len(sorted_img_dir)} images to evaluate")

    processor = ImageProcessor(model_path=MODEL_PATH)

    for img_dir in tqdm(sorted_img_dir[900:]):
        timestamp = float(img_dir.split("_")[-1].split(".jpg")[0])
        img_path = os.path.join(IMG_PATH, img_dir)
        img = cv2.imread(img_path)
        cv_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        numeric_data, _, flag = processor.serialized_processing(cv_img)
        print(
            f"timestamp {timestamp} -- pos_x {numeric_data[0]} -- pos_y {numeric_data[1]} -- kalman_x {numeric_data[2]} -- kalman_y {numeric_data[3]} -- kalman_vel_x {numeric_data[4]} -- kalman_vel_y {numeric_data[5]} -- puncture_flag {flag}"
        )
