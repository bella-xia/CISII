import cv2
import matplotlib.pyplot as plt


def visualize_multi(img_arr, lines=None):
    _, ax = plt.subplots(
        1, len(img_arr) + 1 if lines is not None else len(img_arr), figsize=(15, 5)
    )
    for i, img in enumerate(img_arr):
        ax[i].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax[i].axis("off")

    if lines is not None:
        ax[-1].imshow(cv2.cvtColor(img_arr[0], cv2.COLOR_BGR2RGB))
        ax[-1].axis("off")
        for line in lines:
            x1, y1, x2, y2 = line[0]
            ax[-1].plot([x1, x2], [y1, y2], color="blue", linewidth=1)

    plt.show()


def visualize_singular(img):
    cv2.imshow("", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def visualize_singular_w_lines(img, lines):
    plt.figure(figsize=(5, 3))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    for line in lines:
        x1, y1, x2, y2 = line[0]
        plt.plot([x1, x2], [y1, y2], color="blue", linewidth=1)
    plt.show()


def visualize_singular_w_dot(img, lines, dot):
    _, ax = plt.subplots(1, 2, figsize=(10, 4))
    for i in range(2):
        ax[i].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax[i].axis("off")
        ax[i].scatter(*dot, color="green", s=10)

        if i == 0:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                ax[i].plot([x1, x2], [y1, y2], color="blue", linewidth=1)

    plt.show()
