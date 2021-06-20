import os
import xml.etree.ElementTree as ET
from decimal import Decimal

dirpath = r'D:\work\roadcrackdetection\datasets\train\India\annotations\test'  # 原来存放xml文件的目录
#dirpath = r'D:\work\roadcrackdetection\datasets\train\India\annotations\xmls'  # 原来存放xml文件的目录
newdir = r'D:\work\roadcrackdetection\datasets\train\India\labels'  # 修改label后存放txt的目录
#dirpath = r'India/annotations/xmls'  # 原来存放xml文件的目录
#newdir = r'India/labels'  # 修改label后存放txt的目录




if not os.path.exists(newdir):
    os.makedirs(newdir)

for fp in os.listdir(dirpath):

    root = ET.parse(os.path.join(dirpath, fp)).getroot()

    xmin, ymin, xmax, ymax = 0, 0, 0, 0

    sz = root.find('size')
    width = float(sz.find('width').text)
    height = float(sz.find('height').text)

    filename = root.find('filename').text
    print(fp)
    with open(os.path.join(newdir, fp.split('.')[0] + '.txt'), 'a+') as f:
        for child in root.findall('object'):  # 找到图片中的所有框

            sub = child.find('bndbox')  # 找到框的标注值并进行读取
            sub_label = child.find('name')
            xmin = int(sub.find('xmin').text)
            ymin = int(sub.find('ymin').text)
            xmax = int(sub.find('xmax').text)
            ymax = int(sub.find('ymax').text)
            try:  # 转换成yolov3的标签格式，需要归一化到（0-1）的范围内
                x_center = Decimal(str(round(float((xmin + xmax) / (2 * width)), 6))).quantize(Decimal('0.000000'))
                y_center = Decimal(str(round(float((ymin + ymax) / (2 * height)), 6))).quantize(Decimal('0.000000'))
                w = Decimal(str(round(float((xmax - xmin) / width), 6))).quantize(Decimal('0.000000'))
                h = Decimal(str(round(float((ymax - ymin) / height), 6))).quantize(Decimal('0.000000'))
                print(str(x_center) + ' ' + str(y_center) + ' ' + str(w) + ' ' + str(h))
                if sub_label.text == 'D00':
                    f.write(' '.join([str(0), str(x_center), str(y_center), str(w), str(h) + '\n']))
                if sub_label.text == 'D10':
                    f.write(' '.join([str(1), str(x_center), str(y_center), str(w), str(h) + '\n']))
                if sub_label.text == 'D20':
                    f.write(' '.join([str(2), str(x_center), str(y_center), str(w), str(h) + '\n']))
                if sub_label.text == 'D40':
                    f.write(' '.join([str(3), str(x_center), str(y_center), str(w), str(h) + '\n']))
                if sub_label.text == 'D43':
                    f.write(' '.join([str(4), str(x_center), str(y_center), str(w), str(h) + '\n']))
                if sub_label.text == 'D44':
                    f.write(' '.join([str(5), str(x_center), str(y_center), str(w), str(h) + '\n']))
                if sub_label.text == 'D50':
                    f.write(' '.join([str(6), str(x_center), str(y_center), str(w), str(h) + '\n']))
            except ZeroDivisionError:
                print(filename, '的 width有问题')

            # with open(os.path.join(newdir, fp.split('.')[0] + '.txt'), 'a+') as f:
            #     f.write(' '.join([str(2), str(x_center), str(y_center), str(w), str(h) + '\n']))