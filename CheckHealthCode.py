import datetime
import os
import re
import urllib.request

import cv2
import easyocr
import numpy as np
import pandas as pd
from pyzbar.pyzbar import decode


def ocr_img(image_url):
    reader = easyocr.Reader(['ch_sim', 'en'])
    result = reader.readtext(image_url)
    info = ""
    for item in result:
        info = info + item[1]
    print("图片识别字符串，", re.findall(r"或(.+?)结", info))


def detect_qr_code(image_url):
    frame = cv2.imread(image_url)
    qrcodes = decode(frame)
    print(qrcodes[0].rect)
    x, y, w, h = qrcodes[0].rect
    image_clip = frame[y:(y + w), x:(x + h)]
    detect_qr_color(image_clip)


def detect_qr_color(image):
    gaussian_blur = cv2.GaussianBlur(image, (5, 5), 0)
    hsv = cv2.cvtColor(gaussian_blur, cv2.COLOR_BGR2HSV)
    erode_hsv = cv2.erode(hsv, None, iterations=1)
    green_mask = cv2.inRange(erode_hsv, np.array([35, 43, 35]), np.array([90, 255, 255]))
    cv2.imshow("hsv", hsv)
    cv2.waitKey(0)
    cv2.imshow("green", green_mask)
    cv2.waitKey(0)


def get_img(url):
    request = urllib.request.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                     'like Gecko) Chrome/61.0.3100.0 Safari/537.36')
    file_dir = os.getcwd()
    parent_path = os.path.join(file_dir, 'images')
    check_parent_exists = os.path.exists(parent_path)
    if not check_parent_exists:
        os.makedirs(parent_path)
    file_path = os.path.join(parent_path, datetime.datetime.now().strftime('%Y%m%d'))
    check_exists = os.path.exists(file_path)
    if not check_exists:
        os.makedirs(file_path)
    image_name = file_path + "/" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
    try:
        urllib.request.urlretrieve(url, image_name)
    except Exception as error:
        print('图片下载失败', error)


def get_data():
    pd.set_option('display.max_columns', None)
    df = pd.read_excel('./test.xlsx', index_col=0, header=1)
    print(df)


if __name__ == '__main__':
    # ocr_img('./20211225/20211225003000.jpg')
    # detect_qr_code('./20211225/2021122501010000.jpg')
    # detect_qr_code('./20211225/20211225013054.jpg')
    # detect_qr_color('./20211225/2021122501010000.jpg')
    # detect_qr_color('./20211225/20211225013054.jpg')
    get_data()
