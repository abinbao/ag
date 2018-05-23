# coding:utf-8

"""
 matplotlib
"""

import matplotlib.pyplot as plt
from ag_cal import cal_ag
from ag_cube_v1 import cal_ag_cube

def draw_line_RE(title,list1,list2):
    x1 = list1
    x2 = list2
    count = len(x1)
    y1 = [i for i in range(1,count+1)]
    print y1

    plt.title(title)
    plt.xlabel('次数')
    plt.ylabel('相对误差')
    plt.plot(y1, x1, 'r', label='ag_cube')
    plt.plot(y1, x2, 'b', label='ag')

    plt.legend(bbox_to_anchor=[0.3, 1])
    plt.grid()
    plt.show()


if __name__ == "__main__":
    ag_list = cal_ag()
    ag_cube_list = cal_ag_cube()
    # ag_list = [1,2]
    # ag_cube_list = [3,4]
    draw_line_RE("ag vs ag_cube",ag_cube_list,ag_list)