# coding:utf-8

from base import Point
from gen_log import logging
"""
@desc 数据加载
@param filename 文件名称
		num 读取行数
"""
def load_data(filename,num):

	file = open(filename)
	count = 0 # 统计有多少个数据点
	point_list = []

	while True:
		line = file.readline()
		if not line:
			break
		elif count == num:
			break
		else:
			str_temp = line.encode("utf-8").split()
			lat = str_temp[2] # y 轴
			lon = str_temp[3] # x 轴
			point = Point(float(lon),float(lat))
			point_list.append(point)
		count = count + 1
	logging.warning("共读取 %s 个点" % count)
	return count,point_list

def write_data(filename,content):
	with open(filename,'a') as f:
		f.write(str(content)+"\n")

def read_data(filename):
	result = []
	with open(filename) as f:
		for line in f:
			result.append(line.rstrip())
	return result

if __name__ == "__main__":
	print read_data("laplace_result.txt")