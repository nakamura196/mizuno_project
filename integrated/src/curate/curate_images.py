from PIL import Image
import json

def curate_images(hojo_name):

    with open("../../output/{}/line_place.json".format(hojo_name), "r") as f:
        line_place = json.load(f)

    page_leng = len(line_place)

    print("{} line curation started".format(hojo_name))

    #各ページの各行を切り出す
    for page in range(1, page_leng+1):
        lines = line_place["p{}".format(page)]
        im = Image.open("../../output/{}/preprocessed/back_black/bb_{}_p{}.jpg".format(hojo_name, hojo_name, page))
        line_count = 1
        print("Page {}: curating".format(page))
        for line in lines:
            x1, x2, y1, y2 = line[0], line[1], line[2], line[3]
            copied_im = im.copy()
            cropped_im = copied_im.crop((x1, y1, x2, y2))
            cropped_im.save("../../output/{}/curated_lines/{}_p{}_line{}.jpg".format(hojo_name, hojo_name, page, line_count))
            line_count += 1
        print("Page {}: curating finished".format(page))
