import cv2
import random
import numpy as np
import string
import arabic_reshaper
import os
from bidi.algorithm import get_display
from PIL import ImageFont, ImageDraw, Image
from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET


# recive the height and the width of the image
def generate_random_point(height, width):
    x, y = (random.randint(0, width - round(width * 20 / 100)),
            random.randint(0, height - round(height * 20 / 100)))
    return (x, y)


def generate_random_coordinates(height, width, start_point):
    serial_height = height * 0.088316667
    serial_width = width * 0.169331457
    width_height_ratio = serial_height / serial_width
    target_width = random.randint(
        round(serial_width), round(width - start_point[0]))
    font_size = (target_width / 7) / 22
    target_height = font_size * 22
    if (target_height > height or start_point[1] - target_height < 0):
        return (False, False, False)
    return (target_width, target_height, font_size)


def get_shuffle_serial(size):
    digits = "٠١٢٣٤٥‬٦٧‬٨٩‬‬"
    places = [0, 1, 2, 3, 4, 5, 7, 8, 10, 11]
    new_digits = ""
    for index in range(7):
        i = random.choice(places)
        new_digits = new_digits + digits[i]
    return new_digits


def init():
    global original_images_path
    global original_images
    original_images_path = "orginal/"
    original_images = [join(original_images_path, f) for f in listdir(original_images_path) if
                       isfile(join(original_images_path, f))]


def generate_images(image_count):
    index = 0
    while index < image_count:
        image = random.choice(original_images)
        print(image)
        image = cv2.imread(image)
        height, width = image.shape[:2]
        #start_point = generate_random_point(height, width)
        start_point = (310, 410)
        image_area = height * width
        serial_width, serial_height, serial_font_size = generate_random_coordinates(
            height, width, start_point)
        if serial_width == False:
            index = index - 1
            continue
        serial_width = serial_width * 0.7
        end_point = (round(start_point[0] + serial_width),
                     round(start_point[1] - serial_height))
        serial_area = serial_height * serial_width
        font = cv2.FONT_HERSHEY_SIMPLEX
        print("Image Num #", str(index), "start at :", start_point)
        original_text = get_shuffle_serial(7)
        text = original_text
        reshaped_text = arabic_reshaper.reshape(text)  # correct its shape
        text = get_display(reshaped_text)
        # cv2.putText(image,text,start_point, font, serial_font_size,(0,0,0),random.randint(0,3),cv2.LINE_AA)
        # cv2.rectangle(image,start_point,(round(start_point[0]+serial_width),round(start_point[1]-serial_height)),(0,255,0),0)
        # cv2.circle(image,start_point,2, (0,0,255), -1)
        # cv2.circle(image,end_point, 2, (0,0,255), -1)
        # cv2.imwrite("test.png",image)
        fontpath = "Mirza/Mirza-Regular.ttf"
        font = ImageFont.truetype(fontpath, round(serial_height * 1.7))
        img_pil = Image.fromarray(image)
        draw = ImageDraw.Draw(img_pil)
        d = (start_point[0], start_point[1] - serial_height)
        draw.text(d, text, font=font, fill=(0, 0, 0))
        # draw.rectangle((start_point,end_point))
        image = np.array(img_pil)
        cv2.imwrite("dataset/" + str(index) + ".png", image)
        # cv2.imshow("test",image)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        index += 1


def generate_xml():
    annotation = ET.Element('annotation')
    folder = ET.SubElement(annotation, 'folder')
    filename = ET.SubElement(annotation, 'filename')
    path = ET.SubElement(annotation, 'path')
    source = ET.SubElement(annotation, 'source')
    database = ET.SubElement(source, 'database')
    size = ET.SubElement(annotation, 'size')
    _width = ET.SubElement(size, 'width')
    _height = ET.SubElement(size, 'height')
    depth = ET.SubElement(size, 'depth')
    segmented = ET.SubElement(annotation, 'segmented')
    _object = ET.SubElement(annotation, 'object')
    name = ET.SubElement(_object, 'name')
    pose = ET.SubElement(_object, 'pose')
    truncated = ET.SubElement(_object, 'truncated')
    difficult = ET.SubElement(_object, 'difficult')
    bndbox = ET.SubElement(_object, 'bndbox')
    xmin = ET.SubElement(bndbox, 'xmin')
    ymin = ET.SubElement(bndbox, 'ymin')
    xmax = ET.SubElement(bndbox, 'xmax')
    ymax = ET.SubElement(bndbox, 'ymax')

    folder.text = "dataset"
    filename.text = str(index) + ".png"
    path.text = join(join(os.getcwd(), "dataset"), str(index) + ".png")
    database.text = "Unknown"
    _width.text = str(width)
    _height.text = str(height)
    depth.text = "3"
    segmented.text = "0"
    name.text = "serial"
    pose.text = "Unspecified"
    truncated.text = "0"
    difficult.text = "0"
    xmin.text = str(round(start_point[0]))
    ymin.text = str(round(start_point[1] - serial_height))
    xmax.text = str(round(end_point[0]))
    ymax.text = str(round(end_point[1] + serial_height))

    # create a new XML file with the results
    mydata = None
    myfile = None
    mydata = ET.tostring(annotation)
    myfile = open("dataset/xml/" + str(index) + ".xml", "wb")
    print(mydata)
    if mydata.endswith(b">>"):
        mydata = mydata[:-1]
    myfile.write(mydata)
    index = index + 1


def main():
    init()
    generate_images(1)


if __name__ == '__main__':
    main()
