from PIL import Image
import os

#背景処理（閾値以下の画素を真っ黒にする）
def boundaryCheck(hojo_name, page):

    if not os.path.exists("../output/{}/experiment/boundaryCheck".format(hojo_name)):
        os.makedirs("../output/{}/experiment/boundaryCheck".format(hojo_name))

    #開いてグレースケール化
    im = Image.open("../images/{0}/p{1}/{0}_p{1}.jpg".format(hojo_name, page))
    width, height = im.size
    im = im.convert("L")

    #チェックするboundaryを読み込む
    boundary = 0
    while True:
        print("Set boundary value (default:100(enter), range:0-255)")
        ans = input()
        if ans == "":
            boundary = 100
            break
        else:
            boundary = int(ans)
            if ans >= 0 and ans < 256:
                break

    #画素値がboundary以下を黒にする
    for x in range(width):
        for y in range(height):
            brightness = im.getpixel((x, y))
            if brightness < boundary:
                im.putpixel((x, y), 0)

    im.save("../output/{}/experiment/boundaryCheck/b{}_p{}.jpg".format(hojo_name, boundary, page))

    print("saved at ../output/{}/experiment/boundaryCheck".format(hojo_name))

if __name__ == "__main__":
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
    print("select page number")
    page = int(input())
    boundaryCheck(hojo_name, page)
