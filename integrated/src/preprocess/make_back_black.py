


def make_back_black(iter_):
    hojo_name = iter_[0]
    page = iter_[1]
    line_interval = iter_[2]
    print("Page {} background processing started".format(page))

    #最終的にはline_intervalに応じてboundaryを変えるかもしれない
    im = Image.open("../../output/preprocessed/filtered/filtered_{}_p{}.jpg".format(hojo_name, hojo_name, page))
    boundary = 100
    im = im.convert("L")

    #画素値がboundary以下を黒にする
    for x in range(w):
        for y in range(h):
            brightness = im.getpixel((x, y))
            if brightness < boundary:
                im.putpixel((x, y), 0)

    im.save("../../output/{}/preprocessed/back_black/bb_{}_p{}.jpg".format(hojo_name, hojo_name, page))

    print("finished background processing page {}".format(page))
