from PIL import Image
import os

def resize():
    RESIZE_RATIO = 3

    query_path = "../query/query.jpg"

    query = Image.open(query_path)
    weight, height = query.size
    resized_query = query.resize((int(weight/RESIZE_RATIO),int(height/RESIZE_RATIO)))
    resized_query.save("../query/resized.jpg")

def filter():
    im = Image.open("../query/resized.jpg")
    w, h = im.size

    im.filter(ImageFilter.MedianFilter(size=3))
    im.save("../query/filtered.jpg")

def back_black(characterIsBlack=False):
    im = Image.open("../query/filtered.jpg")
    width, height = im.size
    im = im.convert("L")

    if characterIsBlack:
        #白背景なら画素値がboundary以上を白にする
        boundary = 155
        for x in range(width):
            for y in range(height):
                brightness = im.getpixel((x, y))
                if brightness > boundary:
                    im.putpixel((x, y), 255)
    else:
        #黒背景なら画素値がboundary以下を黒にする
        boundary = 100
        for x in range(width):
            for y in range(height):
                brightness = im.getpixel((x, y))
                if brightness < boundary:
                    im.putpixel((x, y), 0)

    im.save("../query/preprocessed.jpg")
