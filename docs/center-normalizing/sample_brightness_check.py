from PIL import Image

print("enter the name of hojo")
hojo_name = input()
im = Image.open("./input/{}.jpg".format(hojo_name)).convert("L")
w, h = im.size

for i in range(10):
    boundary = 50 + i*10
    im_cop = im.copy()
    for x in range(w):
        for y in range(h):
            px = im_cop.getpixel((x, y))
            if px <= boundary:
                im_cop.putpixel((x, y), 0)
    im_cop.save("./output/brightcheck_b{}.jpg".format(boundary))
    print("boundary-{} processing finished".format(boundary))
