# coding:utf-8
import sys
import os
from gen_log import logging
from gen_log import log
import time
import matplotlib.pyplot as plt
cities= "./citys"

# 获取当前目录下的所有文件
def list_dirs(path):
	parents = os.listdir(path)
	return parents

LOG = log("cities.log")

def read_dat(path, num):
	file = open(path)
	count = 0
	x_list = []
	y_list = []
	while True:
		line = file.readline()
		if not line:
			break
		elif count == num:
			break
		elif count <3:
			count = count + 1
			continue
		else:
			str_temp = line.split("|")
			if len(str_temp[3].strip()) != 0:
				lat = str_temp[3]  # y 轴
				lon = str_temp[4]  # x 轴
				x_list.append(lon)
				y_list.append(lat)
			count = count + 1
	return x_list, y_list

# 读取各个文件中的坐标
def read_data(filename, num):
	file = open(filename)
	count = 0  # 统计有多少个数据点

	x_list = []
	y_list = []
	while True:
		line = file.readline()
		if not line:
			break
		elif count == num:
			break
		else:
			str_temp = line.split()
			lat = str_temp[2].split(',')[0]  # y 轴
			lon = str_temp[2].split(',')[1]  # x 轴
			x_list.append(lon)
			y_list.append(lat)
		count = count + 1
	return x_list, y_list

# 画图
def paint_xy(x,y,photo):
    plt.scatter(x, y,s=20,alpha=0.5,c="b",edgecolors=None,marker=".")
    plt.xlim(-160,160)
    plt.ylim(-80,80)
    plt.xlabel("latitude")
    plt.ylabel("longitude")
    plt.show()


if __name__ == "__main__":
	start_temp = time.time()
	starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_temp))
	LOG.warning("Start loading data,  %s" % starttime)
	files = list_dirs(cities)
	LOG.warning("共有城市文件个数： %s" % str(len(files)))

	x_list = [] # 存储 x 坐标
	y_list = [] # 存储 y 坐标

	# for file in files:
	# 	x, y = read_data(cities + "/" + file,100)
	# 	x_list.extend(x)
	# 	y_list.extend(y)

	x,y = read_dat("./checkins.dat",1000000)
	x_list.extend(x)
	y_list.extend(y)

	LOG.warning("共读取坐标点个数：%s" % str(len(x_list)))

	LOG.warning("开始画图啦....")
	paint_xy(x_list,y_list, "./images/ll.png")
	LOG.warning("画完啦...")

	end_temp = time.time()
	endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_temp))
	LOG.warning("End loading data...,  %s" % endtime)
	LOG.warning("共花费时间：%s" % (end_temp - start_temp))