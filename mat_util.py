# coding:utf-8

"""
 matplotlib
"""

import matplotlib.pyplot as plt
from ag_cal import cal_ag
from ag_cube_v1 import cal_ag_cube
from load_data import load_data

def draw_line_RE(title,list1,list2):
    x1 = list1
    x2 = list2
    count = len(x1)
    y1 = [i for i in range(1,count+1)]

    plt.title(title)
    plt.xlabel('次数')
    plt.ylabel('相对误差')
    plt.plot(y1, x1, 'r', label='ag_cube')
    plt.plot(y1, x2, 'b', label='ag')

    plt.legend(bbox_to_anchor=[0.3, 1])
    plt.grid()
    plt.show()

def paint(result,result_ag):

    ag_list = [i for i in range(0,6)]
    ag_cube_list = [i for i in range(0,6)]
    y1 = [i for i in range(0,6)]

    for item in result:
        if item == "6,3":
            y1[0] = item
            ag_list[0] = result_ag[item]
            ag_cube_list[0] = result[item]
        if item == "12,6":
            y1[1] = item
            ag_list[1] = result_ag[item]
            ag_cube_list[1] = result[item]
        if item == "24,12":
            y1[2] = item
            ag_list[2] = result_ag[item]
            ag_cube_list[2] = result[item]
        if item == "48,24":
            y1[3] = item
            ag_list[3] = result_ag[item]
            ag_cube_list[3] = result[item]
        if item == "96,48":
            y1[4] = item
            ag_list[4] = result_ag[item]
            ag_cube_list[4] = result[item]
        if item == "192,96":
            y1[5] = item
            ag_list[5] = result_ag[item]
            ag_cube_list[5] = result[item]
        # y1.append(str(item))
        # ag_cube_list.append(result[item])
        # ag_list.append(result_ag[item])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    xdata = range(len(ag_cube_list))
    plt.plot(xdata, ag_cube_list, "b-",label="ag_cube",marker="o")
    plt.plot(xdata, ag_list, "r-",label="ag",marker="o")
    ax.set_xticks(range(len(y1)))
    ax.set_xticklabels(y1)
    plt.title("")
    plt.xlabel("square")
    plt.ylabel("relative error")
    # ax.set_yticks([1.4, 1.6, 1.8])

    # grow the y axis down by 0.05
    # ax.set_ylim(1.35, 1.8)
    # expand the x axis by 0.5 at two ends
    # ax.set_xlim(-0.5, len(labels) - 0.5)
    plt.legend(bbox_to_anchor=[0.3, 1])
    plt.grid()
    plt.show()

def paint_xy():
    x,y = load_data("simple.txt",100000)
    plt.scatter(x, y,s=20,alpha=0.5,c="b",edgecolors=None,marker=".")
    plt.xlim(-160,160)
    plt.ylim(-80,80)
    plt.xlabel("latitude")
    plt.ylabel("longitude")
    plt.show()




if __name__ == "__main__":
    # ag_list = cal_ag()
    # ag_cube_list = cal_ag_cube()
    # ag_list = [1,2]
    # ag_cube_list = [3,4]
    # draw_line_RE("ag vs ag_cube",ag_cube_list,ag_list)
    paint_xy()