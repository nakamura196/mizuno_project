import json, os
from PIL import Image, ImageDraw

hojos = os.listdir("../input/images/")
if ".DS_Store" in hojos:
    hojos.remove(".DS_Store")
print("---------hojo list ---------")
idx = 1
for hojo in hojos:
    print("{} {}".format(idx, hojo))
    idx += 1
print("----------------------------")
print("select hojo (enter number)")
ans = int(input())
hojo_name = hojos[ans-1]

with open("../output/{}/line_place/line_place.json".format(hojo_name), "r") as f:
    line_place = json.load(f)
page_leng = len(line_place)

#line_place_for_rewritingがあったら、それに基づいてline_placeを作り直す
if os.path.exists("../output/{}/line_place/line_place_for_rewriting.txt".format(hojo_name)):
    with open("../output/{}/line_place/line_place_for_rewriting.txt".format(hojo_name), "r"):
        lines = [line.strip() for line in f.readlines]
        line_place = {}
        for page in range(1, page_leng+1):
            line_place["p{}".format(page)] = lines[page-1].replace("p{}--".format(page))
        line_place_js = json.dumps(line_place)
        with open("../output/{}/line_place/line_place.json".format(hojo_name), "w"):
            f.write(line_place_js)

#チェックするためのline_placeを見やすくするために、line_place_for_rewritingを作成する
with open("../output/{}/line_place/line_place.json".format(hojo_name), "r") as f:
    line_place = json.load(f)

lines = []
for page in range(1, page_leng+1):
    lines.append("p{}--".format(page) + str(line_place["p{}".append(page)]))

with open("../output/{}/line_place/line_place_for_rewriting.txt".format(hojo_name), "w") as f:
    for line in lines:
        f.write(line)
        f.write("\n")

#指定されたページのline_placeにある範囲を1行ずつ図示し、正しいかどうかを見る
print("Set page number for line-check")
page = int(input)
lines = line_place["p{}".format(page)]
for line in lines:
    #場所を囲った画像を出力
    print("Line place for {} page-{} started".format(hojo_name, page))
    print("Is this line-place OK? Please check")
    x1, x2, y1, y2 = line[0], line[1], line[2], line[3]

    im = Image.open("../input/images/{0}/p{1}/{0}-p{1}.jpg".format(hojo_name, page))
    draw = ImageDraw.Draw(im)
    draw.rectangle((x1, y1, x2, y2), fill=None, outline=(255, 0, 0)) #赤線で囲む
    im.show()
    print("Red square covers: x1(left):{}, x2(right):{}, y1(upper):{}, y2(bottom):{}".format(x1, x2, y1, y2))
    print("If this square is wrong, please rewrite line_place_for_rewriting.txt at ../output/{}/line_place".format(hojo_name))
    print("Is it OK to go next page? (enter for next page, 'n' for exit program)")
    print("\tif you have to rewrite line place, you should enter 'n' and rewrite, then run this program again.")
    ans = input()
    if ans == "n":
        break
