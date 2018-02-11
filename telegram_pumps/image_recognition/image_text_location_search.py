import os
import cv2.text as cv_ext
import cv2 as cv_core
import numpy as np


def process_all_images():
    for file_name in os.listdir(os.path.join(os.getcwd(), 'test_images')):
        print(file_name)
        relative_file_path = 'test_images/' + file_name
        print(relative_file_path)
        if file_name.endswith(".jpg"):

            img = cv_core.imread(relative_file_path, cv_core.CV_64FC3)
            # img = cv_core.imread(relative_file_path, cv_core.IMREAD_GRAYSCALE)
            thr_img = cv_core.adaptiveThreshold(img, 255, cv_core.ADAPTIVE_THRESH_GAUSSIAN_C, cv_core.THRESH_BINARY, 11, 2)

            text_spotter = cv_ext.TextDetectorCNN_create("textbox.prototxt", "TextBoxes_icdar13.caffemodel")

            vis = thr_img.copy()
            rects, out_probs = text_spotter.detect(thr_img)
            threshold = 0.5

            for r in range(np.shape(rects)[0]):
                if out_probs[r] > threshold:
                    rect = rects[r]
                    cv_core.rectangle(vis, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0), 2)

            result_file_path = os.path.join(os.getcwd(), 'test_results/' + file_name)
            print(result_file_path)
            cv_core.imwrite(result_file_path, vis)
