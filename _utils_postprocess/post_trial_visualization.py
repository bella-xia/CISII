import os, cv2, argparse, cv2, sys, re
import pandas as pd
import numpy as np
from tqdm import trange
from tqdm import tqdm
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtGui
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QBrush, QColor

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-fw", "--frame_width", type=int, default=1600)
    parser.add_argument("-fh", "--frame_height", type=int, default=840)
    parser.add_argument("-fr", "--frame_rate", type=int, default=6)
    parser.add_argument(
        "--path",
        type=str,
        default="C:/Users/zhiha/OneDrive/Desktop/Bella_Hanbei_Embryo_Experiments/transfer 03/20250412-170349-190867_TP",
    )
    parser.add_argument("-fm", "--max_frame", type=int, default=50)
    parser.add_argument("-m", "--mode", type=str, default="kalman_demo")

    args = parser.parse_args()

    meta_path = os.path.join(args.path, "ee_csv.csv")

    image_paths = [img for img in os.listdir(args.path) if img.startswith("iOCT")]
    image_paths = sorted(
        image_paths, key=lambda x: float(x.split(".")[0].split("_")[-1])
    )
    mask_paths = [mask for mask in os.listdir(args.path) if mask.startswith("mask")]
    mask_paths = sorted(mask_paths, key=lambda x: float(x.split(".")[0].split("_")[-1]))

    image_idx, mask_idx = 0, 0

    frame_size = (args.frame_width, args.frame_height)

    app = QtWidgets.QApplication([])

    main_window = QtWidgets.QMainWindow()
    central_widget = QtWidgets.QWidget()
    main_window.setCentralWidget(central_widget)

    layout = QtWidgets.QGridLayout()
    central_widget.setLayout(layout)

    # --- Top row: QLabel for images ---
    image_views = []

    for i in range(2):
        pw = pg.PlotWidget()
        pw.setAspectLocked(True)  # Keep aspect ratio consistent
        pw.hideAxis("bottom")
        pw.hideAxis("left")

        img_item = pg.ImageItem()
        pw.addItem(img_item)

        layout.addWidget(pw, 0, i)
        image_views.append((pw, img_item))

    scatter_px = pg.ScatterPlotItem(pen=pg.mkPen(None), brush=pg.mkBrush("g"), size=10)
    scatter_mask = pg.ScatterPlotItem(
        pen=pg.mkPen(None), brush=pg.mkBrush("g"), size=10
    )

    label = pg.TextItem(text="No Puncture", color="green", anchor=(0.5, 0.5))
    image_views[1][0].addItem(label)
    label.setPos(75, 100)

    bounding_box = QGraphicsRectItem(50, 50, 100, 20)
    bounding_box.setPen(pg.mkPen(color="green", width=2))
    green_qcolor = QColor("green")
    green_qcolor.setAlpha(255)
    bounding_box.setBrush(QBrush(green_qcolor))
    image_views[1][0].addItem(bounding_box)
    image_views[0][0].addItem(scatter_px)
    image_views[1][0].addItem(scatter_mask)

    # --- Bottom row: PyQtGraph plot widgets ---
    plot_widgets = []
    plot_lines = []
    titles = [
        "Pre-Kalman Velocity",
        "Post-Kalman Velocity",
    ]
    for title in titles:
        pw = pg.PlotWidget(title=title)
        pw.addLegend()
        pw.setYRange(-50, 50)
        layout.addWidget(pw)
        plot_widgets.append(pw)
        plot_lines.append(pw.plot(pen=pg.mkPen("b", width=2), name="velocity"))
        plot_lines.append(
            pw.plot(pen=pg.mkPen("w", width=2), name="acceleration magnitude")
        )

    main_window.resize(frame_size[0], frame_size[1])
    main_window.show()
    QtWidgets.QApplication.processEvents()

    video_writer = cv2.VideoWriter(
        f"output.avi",
        cv2.VideoWriter_fourcc(*"XVID"),
        30,
        frame_size,
    )

    if os.path.exists(meta_path):
        df = pd.read_csv(meta_path)

    df = df.sort_values(by=["time_puncture"])
    min_time, max_time = (
        df.iloc[0]["time_puncture"],
        df.iloc[-1]["time_puncture"],
    )

    px, py = 640, 480
    dx, dy, kvx, kvy = 0, 0, 0, 0

    lines = [[] for _ in range(5)]

    for idx in trange(0, len(df), 5):

        df_instance = df.iloc[idx]
        timestamp = df_instance["time_puncture"]

        while (
            image_idx < len(image_paths) - 1
            and float(image_paths[image_idx].split(".")[0].split("_")[-1]) < timestamp
        ):
            image_idx += 1
        while (
            mask_idx < len(mask_paths) - 1
            and float(mask_paths[mask_idx].split(".")[0].split("_")[-1]) < timestamp
        ):
            mask_idx += 1
        image_instance = os.path.join(
            args.path, "iOCT_image_{:.10f}.jpg".format(timestamp)
        )

        image = cv2.imread(os.path.join(args.path, image_paths[image_idx]))
        if image.dtype == np.float32 or image.dtype == np.float64:
            image = (
                255 * (image - np.min(image)) / (np.max(image) - np.min(image))
            ).astype(np.uint8)
        elif image.dtype != np.uint8:
            image = image.astype(np.uint8)

        image = np.transpose(np.flipud(image), (1, 0, 2))

        image_views[0][1].setImage(image)

        mask = cv2.imread(
            os.path.join(args.path, mask_paths[mask_idx]),
            cv2.IMREAD_GRAYSCALE,
        )
        mask = (mask * 255).astype(np.uint8)

        y_indices, x_indices = np.where(mask > 0.1)
        if len(y_indices) == 0:
            pos_x, pos_y = -1, -1
        else:
            pos_y = np.min(y_indices)
            pos_x = np.min(x_indices[y_indices == pos_y])

        mask = np.transpose(np.flipud(mask), (1, 0))
        image_views[1][1].setImage(mask)

        if pos_x == -1 or pos_y == -1:
            scatter_mask.setData([], [])
        else:
            scatter_mask.setData([pos_x], [480 - pos_y])
        scatter_px.setData([], [])

        px_t, py_t = (
            df_instance["segment_pos_x"],
            df_instance["segment_pos_y"],
        )
        kvx_t, kvy_t = (
            df_instance["kalman_vel_x"],
            df_instance["kalman_vel_y"],
        )

        flag = df_instance["puncture_image_flag"]

        if flag == 0:
            instance_color = "green"
            instance_text = "No Puncture"
        else:
            instance_color = "blue"
            instance_text = "Puncture"
        qcolor = QColor(instance_color)
        qcolor.setAlpha(255)
        bounding_box.setPen(pg.mkPen(color=instance_color, width=2))
        bounding_box.setBrush(QBrush(qcolor))
        label.setColor(instance_color)
        label.setText(instance_text)

        if min([px_t, py_t]) == -1:
            px_t, py_t = 640, 480
            dx_t, dy_t, d_t = 0, 0, 0
            kvx_t, kvy_t = 0, 0

        else:
            dx_t, dy_t = px_t - px, py_t - py
            sign = 1 if dy_t < 0 else -1
            d_t = sign * np.sqrt(dx_t**2 + dy_t**2)

            ax_t, ay_t = dx_t - dx, dy_t - dy
            a_t = np.sqrt(ax_t**2 + ay_t**2)

            sign = 1
            # if kvy_t < 0 else -1
            kv_t = sign * np.sqrt(kvx_t**2 + kvy_t**2)

            kax_t, kay_t = kvx_t - kvx, kvy_t - kvy
            ka_t = np.sqrt(kax_t**2 + kay_t**2)

        px, py = px_t, py_t
        dx, dy, kvx, kvy = dx_t, dy_t, kvx_t, kvy_t
        lines[0].append(df_instance["time_puncture"])

        # first plot
        lines[1].append(d_t)
        lines[2].append(a_t)

        lines[3].append(kv_t)
        lines[4].append(ka_t)

        for idx in range(2):
            plot_lines[2 * idx].setData(
                lines[0][-args.max_frame :],
                lines[2 * idx + 1][-args.max_frame :],
            )
            plot_lines[2 * idx + 1].setData(
                lines[0][-args.max_frame :],
                lines[2 * idx + 2][-args.max_frame :],
            )

        QtWidgets.QApplication.processEvents()
        img = central_widget.grab().toImage()
        buffer = img.bits().asstring(img.byteCount())
        arr = np.frombuffer(buffer, dtype=np.uint8).reshape(
            (img.height(), img.width(), 4)
        )
        bgr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

        video_writer.write(bgr)

    video_writer.release()
