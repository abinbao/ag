# coding:utf-8

import sys
reload(sys)
import time

import math
import numpy as np
import logging.handlers
import logging
from laplace import cal_abs_rate
from load_data import write_data
from config import e,res_num,read_num,test_query_square,origin_square
"""
日志
"""
# 日志
LOG_FILE = 'ag.log'
logging.basicConfig()
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger('')
logger.addHandler(handler)
logger.setLevel(logging.WARN)

"""
@desc:
	统计共有多少个数据点
"""
def count_point(filename,num):
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
			lat = str_temp[2]
			lon = str_temp[3]
			loc_point = []
			loc_point.append(float(lon)) # x轴
			loc_point.append(float(lat)) # y轴
			point_list.append(loc_point)
		count = count + 1
	return count,point_list

# 统计 m1 的只  共分 m1*m1 个网格
def cal_grid_num(n,e,c):

	m = max(10,math.ceil(0.25*math.sqrt((n*e)/c)))

	return m
# 统计 m2 共分 m2*m2 个网格
def cal_grid_m2(N,a,e,c):
	m2 = math.ceil(math.sqrt(N*(1-a)*e/c))
	return m2
"""
第一次 划分网格
"""
def divide_grid(square_list,num,x,y):

	x_unit = float(x)/float(num) # 横坐标单元格宽度 
	y_unit = float(y)/float(num) # 纵坐标单元长度

	y_bottom = -(y/2)
	x_bottom = -(x/2)
	for i in range(0,num):
		x_tup = []
		x_tup.append(x_bottom)
		x_tup.append(float('%.2f' % (x_bottom + x_unit)))
		temp = y_bottom
		for i in range(0,num):
			y_tup = []
			y_tup.append(temp)
			y_tup.append(temp+y_unit)
			square = []
			square.append(x_tup)
			square.append(y_tup)
			temp = temp+y_unit
			square_list.append(square)
		x_bottom = float('%.2f' % (x_bottom + x_unit))
	return square_list

"""
第二次划分网格
"""

def divide_grid2(square_list_2,result_laplace,item):
	x1 = float(item.split("&&")[0].split(",")[0])
	x2 = float(item.split("&&")[0].split(",")[1])
	y1 = float(item.split("&&")[1].split(",")[0])
	y2 = float(item.split("&&")[1].split(",")[1])
	# 参数 N a e c
	m2 = cal_grid_m2(float(result_laplace[item]),0.5,0.1,5)
	x_unit = float(x2-x1)/float(m2)
	y_unit = float(y2-y1)/float(m2)

	x_bottom = x1
	y_bottom = y1
	for i in range(0, int(m2)):
		x_tup = []
		x_tup.append(x_bottom)
		x_tup.append(float('%.2f' % (x_bottom + x_unit)))
		temp = y_bottom
		for i in range(0, int(m2)):
			y_tup = []
			y_tup.append(temp)
			y_tup.append(temp + y_unit)
			square = []
			square.append(x_tup)
			square.append(y_tup)
			temp = temp + y_unit
			square_list_2.append(square)
		x_bottom = float('%.2f' % (x_bottom + x_unit))
	return square_list_2

# 统计每个区域 点的个数

def cal_point_num(square_list,point_list,depth):
	result_act = {}
	for i in range(0,len(square_list)):
		for j in range(0,len(point_list)):
			square = str(square_list[i][0][0]) + "," + str(square_list[i][0][1]) + "&&" + str(square_list[i][1][0]) + "," + str(square_list[i][1][1])
			if point_list[j][0] >= square_list[i][0][0] and point_list[j][0] <= square_list[i][0][1] and point_list[j][1] >= square_list[i][1][0] and point_list[j][1] <= square_list[i][1][1]:

				try:
					result_act[square] = result_act[square] + 1
				except :
					result_act[square] = 1

	return result_act

# 拉普拉斯噪声
def laplace_noise(loc,scale,size):
	s = np.random.laplace(loc, scale, size)
	return s

# 加入拉普拉斯噪声的 区域点
def lapalce_grid_point_num(grid_points):
	result_laplace = {}
	for i in grid_points:
		result_laplace[i] = grid_points[i] + laplace_noise(0,0.1,1)[0]
	return result_laplace

# 查询区域 laplace噪声  个数
"""
x1 x2 y1 y2 查询区域
result_laplace 加入拉普拉斯噪声的各个区域中包含点的个数
"""
def search_square_laplace_point_num(x1,x2,y1,y2,result_laplace):

	count = 0
	# 遍历 拉普拉斯噪声
	for item in result_laplace:
		x_list = item.split("&&")[0]
		y_list = item.split("&&")[1]
		x3 = float(x_list.split(",")[0])
		x4 = float(x_list.split(",")[1])
		y3 = float(y_list.split(",")[0])
		y4 = float(y_list.split(",")[1])
		# 区域面积
		square = (x4-x3)*(y4-y3)
		# 1. 全部在区域中
		if x3 >=x1 and x4<=x2 and y3>=y1 and y4 <= y2:
			count = count + result_laplace[item]
		# 2. 左上角
		elif x3 <=x1 and x4 >=x1 and x4 <=x2 and y3 >= y1 and y3 <=y2 and y4 >=y2:
			rate = (x4-x1)*(y2-y3)/square
			count = count + result_laplace[item]*rate
		# 3. 左边
		elif x3 <= x1 and x4 >= x1 and x4 <= x2 and y3 >= y1 and y4 <=y2:
			rate = (x4-x1)*(y4-y3)/square
			count = count + result_laplace[item]*rate
		# 4. 左下角
		elif x3 <= x1 and x4 >= x1 and x4 <=x2 and y3 <=y1 and y4 >= y1 and y4 <= y2:
			rate = (x4-x1)*(y4-y1)/square
			count = count + result_laplace[item]*rate
		# 5. 下边
		elif x3 >= x1 and x4 <= x2 and y3 <= y1 and y4 >=y1 and y4 <= y2:
			rate = (x4-x3)*(y4-y1)/square
			count = count + result_laplace[item]*rate
		# 6. 右下角
		elif x3 >= x1 and x3 <= x2 and x4 >= x2 and y3 <= y1 and y4 >= y1 and y4 <= y2:
			rate = (x2-x3)*(y4-y1)/square
			count = count + result_laplace[item]*rate
		# 7. 右边
		elif x3 >= x1 and x3 <= x2 and x4 >= x2 and y3>= y1 and y4 <= y2:
			rate = (x2-x3)*(y4-y3)/square
			count = count + result_laplace[item]*rate
		# 8. 右上角
		elif x3 >= x1 and x3 <= x2 and x4 >= x2 and y3>=y1 and y3 <= y2 and y4 >= y2:
			rate = (x2-x3)*(y2-y3)/square
			count = count + result_laplace[item]*rate
		# 9. 上边
		elif x3 >= x1 and x4 <= x2 and y3>=y1 and y3 <=y2 and y4 >= y2:
			rate = (x4-x3)*(y2-y3)/square
			count = count + result_laplace[item]*rate
	return count


# 查询区域 实际 个数
def search_square_actual_point_num(x1,x2,y1,y2,point_list):
	count = 0
	for item in point_list:
		x_loc = item[0]
		y_loc = item[1]
		if x_loc >=x1 and x_loc <=x2 and y_loc >= y1 and y_loc <= y2:
			count  = count + 1
	return count

def main(query_square):

	# 读取样本数据 filename样本文件名称，num 读取行数
	count,point_list = count_point("simple.txt",read_num)
	# logging.warning("读取样本数量：%s 行,样本数据点为：%s" % (str(count),point_list))

	square_list = []
	"""
	第一次划分网格个数
	"""
	m1 = cal_grid_num(count,0.1,10)
	# logging.warning("第一次网格划分个数：%d"  % int(m1))
	divide_grid(square_list,int(m1),origin_square[0],origin_square[1])
	# logging.warning("第一次划分网格区域数量：%d , 网格区域为：%s" % (len(square_list),square_list))

	"""
	统计每个区域的 点的个数 并加入噪声，获得 N，计算 m2
	"""
	# 统计各个区域的点的个数
	result_act = cal_point_num(square_list, point_list,1)
	# logging.warning("实际区域分布：%s" % result_act)
	# 统计加入拉普拉斯噪声后 各个区域的点
	result_laplace = lapalce_grid_point_num(result_act)
	# logging.warning("拉普拉斯噪声:%s" % result_laplace)


	square_list_2 = [] # 第二次划分网格
	"""
	第二次划分网格
	"""
	for item in result_laplace:
		divide_grid2(square_list_2,result_laplace,item)

	# logging.warning("第二次划分网格：%s" % square_list_2)

	"""
	统计每个区域 加入拉普拉斯噪声 的点数
	"""
	result_act1 = cal_point_num(square_list_2,point_list,2)
	# logging.warning( "第二次实际区域分布：%s" % result_act1)
	result_laplace1 = lapalce_grid_point_num(result_act1)
	# logging.warning( "第二次拉普拉斯噪声:%s" % result_laplace)

	# 计算查询区域的点的个数  拉普拉斯
	laplace_num = search_square_laplace_point_num(query_square[0],query_square[1],query_square[2],query_square[3],result_laplace1)
	logging.warning("拉普拉斯-查询区域点个数：%s" % laplace_num)
	# 计算查询区域实际点的个数
	act_num = search_square_actual_point_num(query_square[0],query_square[1],query_square[2],query_square[3],point_list)
	logging.warning("实际-查询区域点个数：%s" % act_num)
	return laplace_num,act_num,count

def cal_ag():
	start_temp = time.time()
	starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_temp))
	logging.warning("Start loading data,  %s" % starttime)
	result = []
	for i in range(0, res_num):
		laplace_num, act_num, count = main(test_query_square)
		RE = cal_abs_rate(laplace_num, act_num, count)
		write_data("ag_result.txt", RE)
		result.append(RE)
	end_temp = time.time()
	endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_temp))
	logging.warning("End loading data...,  %s" % endtime)
	logging.warning("共花费时间：%s" % (end_temp - start_temp))
	return result

def cal_ag_param(param):
	query_square = []
	query_square.append(param.x1)
	query_square.append(param.x2)
	query_square.append(param.y1)
	query_square.append(param.y2)
	laplace_num, act_num, count = main(query_square)
	RE = cal_abs_rate(laplace_num, act_num, count)

	return RE

if __name__ == '__main__':
	cal_ag()
	# cal_ag_param()


