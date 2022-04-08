import datetime
import os
import re
import time
import urllib.request

import paddlehub as hub
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
        print(item.text)
    print('图片文字识别内容：', info)
    print("途径区域：", re.findall(r"或(.+?)结", info))
    print("健康码颜色:", re.findall(r"绿码", info))


def ocr_paddle(image_url):
    ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
    result = ocr.recognize_text(images=[cv2.imread(image_url)])
    info = ""
    datasets = result[0]['data']
    for dateset in datasets:
        info = info + dateset['text']
    print("途径区域：", re.findall(r"或(.+?)结", info))
    print("健康码颜色:", re.findall(r"绿码", info))
    print(info)


# def ocr_health_code(image_url):
#     reader = easyocr.Reader(['ch_sim', 'en'])
#     result = reader.readtext(image_url)
#     info = ""
#     for item in result:
#         info = info + item[1]
#
#
# def detect_qr_code(image_url):
#     frame = cv2.imread(image_url)
#     qrcodes = decode(frame)
#     print(qrcodes[0].rect)
#     x, y, w, h = qrcodes[0].rect
#     image_clip = frame[y:(y + w), x:(x + h)]
#     detect_qr_color(image_clip)
#
#
# def detect_qr_color(image):
#     gaussian_blur = cv2.GaussianBlur(image, (5, 5), 0)
#     hsv = cv2.cvtColor(gaussian_blur, cv2.COLOR_BGR2HSV)
#     erode_hsv = cv2.erode(hsv, None, iterations=1)
#     green_mask = cv2.inRange(erode_hsv, np.array([35, 43, 35]), np.array([90, 255, 255]))
#     cv2.imshow("hsv", hsv)
#     cv2.waitKey(0)
#     cv2.imshow("green", green_mask)
#     cv2.waitKey(0)
#
#
# def get_img(url):
#     request = urllib.request.Request(url)
#     request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
#                                      'like Gecko) Chrome/61.0.3100.0 Safari/537.36')
#     file_dir = os.getcwd()
#     parent_path = os.path.join(file_dir, 'images')
#     check_parent_exists = os.path.exists(parent_path)
#     if not check_parent_exists:
#         os.makedirs(parent_path)
#     file_path = os.path.join(parent_path, datetime.datetime.now().strftime('%Y%m%d'))
#     check_exists = os.path.exists(file_path)
#     if not check_exists:
#         os.makedirs(file_path)
#     image_name = file_path + "/" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
#     try:
#         urllib.request.urlretrieve(url, image_name)
#     except Exception as error:
#         print('图片下载失败', error)
#
#
# def get_data():
#     pd.set_option('display.max_columns', None)
#     df = pd.read_excel('./test.xlsx', index_col=0, header=1)
#     print(df)


def search_file(start_dir):
    img_list = []
    extend_name = ['.jpg', '.png', '.gif']  # 图片格式，可以添加其他图片格式
    os.chdir(start_dir)  # 改变当前工作目录到指定的路径

    for each_file in os.listdir(os.curdir):
        # listdir()返回指定的文件夹包含的文件或文件夹的名字的列表 curdir表示当前工作目录

        img_prop = os.path.splitext(each_file)
        if img_prop[1] in extend_name:
            img_list.append(os.getcwd() + os.sep + each_file)
            # os.getcwd()获得当前路径 os.sep分隔符 os.linesep换行符
    for img in img_list:
        ocr_paddle(img)


if __name__ == '__main__':
    start_dir = './images'
    start = time.perf_counter()
    search_file(start_dir)
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))
    # ocr_img('./images/20211225/20211225003000.jpg')
    # detect_qr_code('./20211225/2021122501010000.jpg')
    # detect_qr_code('./20211225/20211225013054.jpg')
    # detect_qr_color('./20211225/2021122501010000.jpg')
    # detect_qr_color('./20211225/20211225013054.jpg')
    # ocr_health_code('./images/20211225/2021122501010000.jpg')
    # get_data()
    # get_img('url')
