import numpy as np
from scipy import signal

def detect_horizon(color_y, height):
    #y方向の切り出し座標y1, y2を見つける
    y1, y2 = 0, 0
    divide_val = int(sum(color_y)/len(color_y))

    for i in range(height-1):
        if color_y[i] > divide_val and color_y[i+1] < divide_val:
            y1 = i+1
        elif color_y[i] < divide_val and color_y[i+1] > divide_val:
            y2 = i
            break

    return y1, y2

def detect_vertical(color_x, line_interval):
    #x方向の行切り出しを見つける
    color_x_np = np.array(color_x)
    localmins  = signal.argrelmin(color_x_np, order=line_interval)
    x_line_list = localmins[0].tolist()
    x_line_list.append(0)
    x_line_list.sort()
    x_line_list.reverse()

    return x_line_list
