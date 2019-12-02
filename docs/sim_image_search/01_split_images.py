import glob
from PIL import Image
import os


def img_split(im, divided_height, slide_window):
    
    """
    画像を分割する。

    Parameters
    ----------
    im : PIL.JpegImagePlugin.JpegImageFile
        対象画像
    divided_height : int
        分割幅
    slide_window: int
        スライド幅

    Returns
    -------
    buff : list
        分割画像のリスト
    """

    w, h = im.size

    slide_window_num = int(h / slide_window)

    buff = []

    for i in range(slide_window_num):
        start = (i-1) * slide_window
        end = start + divided_height
        if end > h:
            end = h

        cim = im.crop((0, start, w, end))
        buff.append(cim)

    return buff

data_dir = "data"
files = glob.glob(data_dir+"/center_lines/*.jpg")

for i in range(len(files)):
    if i % 100 == 0:
        print(str(i+1))

    filepath = files[i]

    #画像ファイル名の取得
    filename = os.path.basename(filepath)
    filename_wo_ext = os.path.splitext(filename)[0]

    im = Image.open(filepath)
    w, h = im.size

    # 倍率の配列
    ratio_arr = [0.8, 1, 1.2]

    for ratio in ratio_arr:
        divided_height = int(w * ratio)
        slide_window = int(divided_height / 3)

        img_arr = img_split(im, divided_height, slide_window)

        for j in range(len(img_arr)):
            img = img_arr[j]
            # 保存先フォルダの指定
            img.save(data_dir+"/center_images/" + filename_wo_ext + "_" +
                    str(ratio) + "_" + str(j).zfill(4) + ".jpg", "JPEG")
