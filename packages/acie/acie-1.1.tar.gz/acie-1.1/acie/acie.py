#!/usr/bin/env python

import cv2
import numpy as np
from imutils.perspective import four_point_transform
import pytesseract
import re
import sys

# Set your Tesseract OCR engine path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def image_processing(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(
        gray, 128, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    return threshold


def scan_detection(image):

    global document_contour

    document_contour = np.array(
        [[0, 0], [WIDTH, 0], [WIDTH, HEIGHT], [0, HEIGHT]])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(
        threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                document_contour = approx
                max_area = area

    cv2.drawContours(frame, [document_contour], -1, (0, 255, 0), 3)


def extractText(ocr_text):
    ad_no = re.search(r'\b\d{4}\s\d{4}\s\d{4}\b', ocr_text)
    dob = re.search(r'\b\d{2}/\d{2}/\d{4}\b', ocr_text)
    gender = re.search(r'(Male|Female|MALE|FEMALE)', ocr_text)
    name = re.search(r'\b[A-Z][a-z]*(?:\s+[A-Z][a-z]*){1,3}\b', ocr_text)

    if name:
        print("Name:", name.group(0))
    else:
        print("Name not detected.")
    if ad_no:
        print("Aadhaar Number:", ad_no.group(0))
    else:
        print("Aadhaar number not detected.")
    if dob:
        dob = str(dob.group(0))
        dob = dob[:2] + "/" + dob[3:5] + "/" + dob[6:]
        print("DOB:", dob)
    else:
        print("DOB not detected.")
    if gender:
        print("Gender:", gender.group(0))
    else:
        print("Gender not detected.")


def main():
    global HEIGHT, WIDTH, frame

    if len(sys.argv) < 2:
        print("Error: No image path provided")
        return

    image_path = sys.argv[1]
    frame = cv2.imread(image_path)

    scale = 0.5

    font = cv2.FONT_HERSHEY_SIMPLEX

    HEIGHT, WIDTH, _ = frame.shape

    frame_copy = frame.copy()

    scan_detection(frame_copy)

    # cv2.imshow("input", cv2.resize(frame, (int(scale * WIDTH), int(scale * HEIGHT))))

    warped = four_point_transform(frame_copy, document_contour.reshape(4, 2))
    # cv2.imshow("Warped", cv2.resize(warped, (int(scale * warped.shape[1]), int(scale * warped.shape[0]))))

    processed = image_processing(warped)
    processed = processed[10:processed.shape[0] -
                          10, 10:processed.shape[1] - 10]
    # cv2.imshow("Processed", cv2.resize(processed, (int(scale * processed.shape[1]),
    #                                                   int(scale * processed.shape[0]))))

    ocr_text = pytesseract.image_to_string(processed)

    extractText(ocr_text)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
