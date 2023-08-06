import cv2
import numpy as np
import copy
from PIL import Image
import io
import base64


class ImageTools:

    def __init__(self):
        pass

    @staticmethod
    def img_bytes2base64(img):
        return str(base64.b64encode(img), 'utf-8')

    @staticmethod
    def img_base642bytes(img):
        return base64.b64decode(img.split('base64,')[-1])

    @staticmethod
    def img_array2bytes(img):
        return cv2.imencode('.png', img)[-1]

    @staticmethod
    def img_bytes2array(img):
        img = np.frombuffer(img, np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        return img

    @staticmethod
    def img_bytes2pil(img):
        buffer = io.BytesIO(img)
        image = Image.open(buffer)
        return image

    @staticmethod
    def img_base642pil(img):
        bytes_data = ImageTools.img_base642bytes(img)
        buffer = io.BytesIO(bytes_data)
        image = Image.open(buffer)
        return image

    @staticmethod
    def img_pil2bytes(img):
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        image_data = buffer.getvalue()
        return image_data

    @staticmethod
    def img_pil2base64(img):
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        image_data = buffer.getvalue()
        image_data = base64.encodebytes(image_data)
        return image_data.decode('utf8')

    @staticmethod
    def megera_alpha_img(raw_img, new_img):
        if not isinstance(raw_img, np.ndarray):
            raw_img = np.array(raw_img)
        if not isinstance(new_img, np.ndarray):
            new_img = np.array(new_img)
        alpha_img1 = raw_img[:, :, 3] / 255.0
        alpha_img2 = new_img[:, :, 3] / 255.0
        alpha = 1 - (1 - alpha_img1) * (1 - alpha_img2)
        for ii in range(3):
            raw_img[:, :, ii] = (raw_img[:, :, ii] * alpha_img1 * (1 - alpha_img2) + new_img[:, :,
                                                                                     ii] * alpha_img2) / alpha
        raw_img[:, :, 3] = alpha * 255
        return


'''
数据增强模块
'''


def augment(image_raw_data, flip=True, rotate=True, rate=0.5):
    assert 'filepath' in image_raw_data
    assert 'bboxes' in image_raw_data
    assert 'width' in image_raw_data
    assert 'height' in image_raw_data

    image_raw_data_copy = copy.deepcopy(image_raw_data)

    image = cv2.imread(image_raw_data_copy['filepath'])

    rows, cols = image.shape[:2]

    # 做增强的概率
    rate_bound = int(rate * 100)

    # flip翻转
    # cv2.flip: 1水平翻转， 0垂直翻转，-1水平垂直翻转
    if np.random.randint(100) < rate_bound and flip:
        image = cv2.flip(image, 1)
        for bbox in image_raw_data_copy['bboxes']:
            x1 = bbox['x1']
            x2 = bbox['x2']
            bbox['x2'] = cols - x1
            bbox['x1'] = cols - x2

    if np.random.randint(100) < rate_bound and flip:
        image = cv2.flip(image, 0)
        for bbox in image_raw_data_copy['bboxes']:
            y1 = bbox['y1']
            y2 = bbox['y2']
            bbox['y2'] = rows - y1
            bbox['y1'] = rows - y2

    # rotate旋转，度数以逆时针为正向
    # TODO 增加随机角度旋转功能
    if np.random.randint(100) < rate_bound and rotate:
        for bbox in image_raw_data_copy['bboxes']:
            x1 = bbox['x1']
            x2 = bbox['x2']
            y1 = bbox['y1']
            y2 = bbox['y2']
            angle = np.random.choice([90, 180, 270], 1)[0]
            if angle == 90:
                image = np.transpose(image, (1, 0, 2))
                image = cv2.flip(image, 0)
                bbox['x1'] = y1
                bbox['x2'] = y2
                bbox['y1'] = cols - x2
                bbox['y2'] = cols - x1
            elif angle == 180:
                image = cv2.flip(image, -1)
                bbox['x2'] = cols - x1
                bbox['x1'] = cols - x2
                bbox['y2'] = rows - y1
                bbox['y1'] = rows - y2
            elif angle == 270:
                image = np.transpose(image, (1, 0, 2))
                image = cv2.flip(image, 1)
                bbox['x1'] = rows - y2
                bbox['x2'] = rows - y1
                bbox['y1'] = x1
                bbox['y2'] = x2

    image_raw_data_copy['width'] = image.shape[1]
    image_raw_data_copy['height'] = image.shape[0]
    return image_raw_data_copy, image
