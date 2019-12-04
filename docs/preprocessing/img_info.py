from PIL import Image
import json

#黒地の法帖限定
def calculate_hojo_brightness(hojo_img_path):
    im = Image.open(hojo_img_path)
    width, height = im.size

    color_x = [0 for i in range(width)]
    color_y = [0 for i in range(height)]

    for x in range(width):
        for y in range(height):
            brightness = im.getpixel((x, y))
            color_x[x] += brightness
            color_y[y] += brightness

    return color_x, color_y, height

def generate_letter_size(hojo_name, page):
    #Google Cloud Visionからゲットした結果を利用
    with open("./images/{}/rintervals.json".format(hojo_name), "r") as f:
        rintervals = json.load(f)

    rinterval_arg  = "../images/{}/p{}/{}-p{}.jpg".format(hojo_name, page, hojo_name, page)
    relative_line_interval = rintervals[rinterval_arg]

    im = Image.open("./intermediates/{}/pp/pp_{}_p{}.jpg".format(hojo_name, hojo_name, page))
    width, height = im.size

    line_interval = int(width*relative_line_interval)

    return line_interval
