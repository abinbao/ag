# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import time
from dateutil import parser
from pylab import mpl
from numpy import *
import matplotlib.pyplot as plt

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

# time parse
def time_parse(temp):
	return parser.parse(temp)
# compare
def time_compare(param):
	flag = False
	startTime = time_parse("2009-02-01 00:00:00")
	endTime = time_parse("2010-11-01 00:00:00")
	if param > startTime and param < endTime:
		flag = True
	return flag

# load data and write data
def load_data(file,file_output):

	lat_list = []
	lon_list = []

	index = 0 # 统计共多少条数据
	count =0 # 统计多少条符合条件的数据
	for i in range(0,1000000):
		line = file.readline()
		if not line:
			print "Finished..."
			break
		else:
			str_temp = line.encode("utf-8").split()
			time_str = str_temp[1].replace("T"," ").replace("Z"," ")
			lat = str_temp[2]
			lon = str_temp[3]
			# 比较时间大小
			if time_compare(time_parse(time_str)):
				 # file_output.write()
				 loc = lat + " " + lon + "\n"
				 file_output.write(loc)
				 count = count + 1
				 # 散点图
				 lat_list.append(float(lat))
				 lon_list.append(float(lon))
		if index%1000 == 0:
			print "已处理：",index," 条数据。"
		index = index + 1
	print "符合条件：%d条数据." % count
	print "共计：%d条数据." % index
	return lat_list,lon_list
# 散点图
def paint_scatter(param1,param2):
	x = param2
	y = param1
	plt.scatter(x, y,s=4)
	plt.title("王晓滨是智障")
	plt.xlabel("latitude")
	plt.ylabel("longitude")
	plt.show()

def main():
	file = open("simple.txt")
	file_output = open("result.txt","wb")
	lat_list,lon_list = load_data(file,file_output)
	
	file.close()
	file_output.close()
	return lat_list,lon_list
if __name__ == '__main__':

	start_temp = time.time()
	starttime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(start_temp))
	print "Start loading data",starttime
	# 获取数据
	lat_list,lon_list = main()

	end_temp = time.time()
	endtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(end_temp))
	print "End loading data...",endtime
	print "共花费时间：",(end_temp-start_temp)
	paint_scatter(lat_list, lon_list)

