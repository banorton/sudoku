import cv2
from imutils import contours
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pytesseract as pytes


def proc():
    Tk().withdraw()
    filename = askopenfilename()

    # Load image, grayscale, and adaptive threshold
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 57, 5
    )

    # Filter out all numbers and noise to isolate only boxes
    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 1000:
            cv2.drawContours(thresh, [c], -1, (0, 0, 0), -1)

    # Fix horizontal and vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, vertical_kernel, iterations=9)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=4)

    # Sort by top to bottom and each row by left to right
    invert = 255 - thresh
    cnts = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    (cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")

    sudoku_rows = []
    row = []
    for i, c in enumerate(cnts, 1):
        area = cv2.contourArea(c)
        if area < 50000:
            row.append(c)
            if i % 9 == 0:
                (cnts, _) = contours.sort_contours(row, method="left-to-right")
                sudoku_rows.append(cnts)
                row = []

    # Iterate through each box
    # for row in sudoku_rows:
    #     for c in row:
    #         mask = np.zeros(image.shape, dtype=np.uint8)
    #         cv2.drawContours(mask, [c], -1, (255, 255, 255), -1)
    #         # result = cv2.bitwise_and(image, mask)
    #         # result[mask == 0] = 255
    #         cv2.imshow("result", image)
    #         cv2.waitKey(175)

    nums = []
    for row in sudoku_rows:
        for cnt in row:
            if cv2.contourArea(cnt) > 200:
                (x, y, w, h) = cv2.boundingRect(cnt)
                # cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 255), 1)
                num_img = gray[y : y + h, x : x + w]
                num = pytes.image_to_string(num_img)
                nums.append(num)
                print(num)
                # cv2.imshow("", num_img)
                # cv2.waitKey(200)
