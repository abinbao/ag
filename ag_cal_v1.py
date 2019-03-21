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
import threading
"""
日志
"""
# 日志
LOG_FILE = 'ag_v1.log'
logging.basicConfig()
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger('')
logger.addHandler(handler)
logger.setLevel(logging.WARN)
from load_data import load_data
from util import cal_grid_num,divide_grid,cal_point_num,lapalce_grid_point_num,divide_grid2,search_square_laplace_point_num,search_square_actual_point_num


def main(param,count,point_list):

	# 读取样本数据 filename样本文件名称，num 读取行数
	# count,point_list = load_data("simple.txt",read_num)
	# logging.warning("读取样本数量：%s 行,样本数据点为：%s" % (str(count),point_list))

	square_list = []
	"""
	第一次划分网格个数
	"""
	m1 = cal_grid_num(count,0.1,10)
	# logging.warning("第一次网格划分个数：%d"  % int(m1))
	divide_grid(square_list,int(m1),origin_square[0],origin_square[1])
	# logging.warning("第一次划分网格区域数量：%d , 网格区域为：%s" % (len(square_list),square_list))

	# 统计各个区域的点的个数,同时计算了lapalce
	cal_point_num(square_list, point_list)


	# 第二次划分网格
	for item in square_list:
		divide_grid2(item)
	for item in square_list:
		cal_point_num(item.square_col, point_list)

	# 计算查询区域的点的个数  拉普拉斯
	count_laplace_num = {"num": 0}
	for item in square_list:
		if len(item.square_col) == 0:
			search_square_laplace_point_num(param.x1, param.x2, param.y1, param.y2, item, count_laplace_num, param)
		else:
			for attr1 in item.square_col:
				search_square_laplace_point_num(param.x1, param.x2, param.y1, param.y2, attr1, count_laplace_num,param)

	# logging.warning("已统计区域个数为：%s" % count_num_square)

	# ？
	logging.warning("拉普拉斯-查询区域点个数：%s" % count_laplace_num["num"])
	# 计算查询区域实际点的个数
	act_num = search_square_actual_point_num(param.x1, param.x2, param.y1, param.y2, point_list)
	logging.warning("实际-查询区域点个数：%s" % act_num)
	return count_laplace_num["num"], act_num, count

def cal_ag():
	countNum, point_list = load_data("simple.txt", read_num)
	start_temp = time.time()
	starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_temp))
	logging.warning("Start loading data,  %s" % starttime)
	laplace_num, act_num, count = main(test_query_square,countNum, point_list)
	RE = cal_abs_rate(laplace_num, act_num, count)
	print RE
	end_temp = time.time()
	endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_temp))
	logging.warning("End loading data...,  %s" % endtime)
	logging.warning("共花费时间：%s" % (end_temp - start_temp))

"""
@:param param 查询区域 countNum 点的个数 point_list 点的集合
"""
def cal_ag_param(param,countNum,point_list):

	laplace_num, act_num, count = main(param,countNum,point_list)
	RE = cal_abs_rate(laplace_num, act_num, count)

	return RE

if __name__ == '__main__':
	cal_ag()
	# cal_ag_param()


