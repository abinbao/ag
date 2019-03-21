# coding:utf-8
"""
@author:xiaobin
@desc: ag_cube
@date: 2018-05-14
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import time
from util import cal_grid_m2,\
	cal_grid_num,\
	divide_grid,\
	divide_grid2,\
	cal_point_num,\
	genrate_line_x,\
	genrate_line_y,\
	cal_valueOfH,\
	find_gold_line,\
	recursion_merge,\
	recursion_print,search_square_actual_point_num,\
    search_square_laplace_point_num
from gen_log import logging
from load_data import load_data,write_data
from laplace import cal_abs_rate
from config import read_num,test_query_square,res_num,origin_square,e

# 主函数
def main(param,count,point_list):

	# 加载经纬度集合 count:加载点的个数  point_list:点的集合
    # count,point_list = load_data("simple.txt",read_num)

    square_list = [] # 区域集合

    # 第一次划分网格个数
    m1 = cal_grid_num(count, 0.1, 10)
    logging.warning("第一次划分网格个数为：%s" % m1)

    # 第一次划分网格
    divide_grid(square_list, int(m1), origin_square[0], origin_square[1])
    logging.warning("第一次划分网格区域数量：%d " % (len(square_list)))

	# 统计各个区域点的个数
    cal_point_num(square_list, point_list)

    # 第二次划分网格
    for item in square_list:
        divide_grid2(item)
	# 统计第二次划分网络各个区域中的个数
    for item in square_list:
		cal_point_num(item.square_col,point_list)
    logging.warning("=========== Starting AG ===========")
    AG_count_laplace_num = {"num":0}
    for item in square_list:
        if len(item.square_col) == 0:
			search_square_laplace_point_num(param.x1, param.x2, param.y1, param.y2, item, AG_count_laplace_num, param)
        else:
            for ii in item.square_col:
            	search_square_laplace_point_num(param.x1, param.x2, param.y1, param.y2, ii, AG_count_laplace_num, param)

    AG_act_num = search_square_actual_point_num(param.x1, param.x2, param.y1, param.y2, point_list)
    logging.warning("AG----actual point number is:  %s" % AG_act_num)
    logging.warning("AG----add laplace point number is:  %s" % AG_count_laplace_num["num"])

    logging.warning("========== Starting AG_CUBE =========")
	# 计算 H 判断区域是否需要继续划分
    for attr1 in square_list:
		for attr2 in attr1.square_col:
			# 划分网格
			# if len(attr2.square_col) == 0:
			# 	continue
			divide_grid2(attr2)
			# 统计各个网格的分割区域个数
			cal_point_num(attr2.square_col, point_list)
			# 生成 遍历线
			genrate_line_x(attr2)
			genrate_line_y(attr2)
			# 判断是否需要继续划分，如果需要 返回 True, 不需要 返回 False
			# 第一个参数 设定的阈值
			cal_valueOfH(e, attr2)

			# 如果 flag = True, 对该区域继续分割, 并找出最分割最平均的分割线
			if attr2.flag:
				find_gold_line(attr2,point_list)
				recursion_merge(attr2.square_D1,point_list)
				recursion_merge(attr2.square_D2,point_list)
			else:
				attr2.square_col = None
    # 计算查询区域的点的个数  拉普拉斯
    count_num_square = 0
    count_laplace_num = {"num":0}
    for item in square_list:
        if len(item.square_col) == 0:
			search_square_laplace_point_num(param.x1, param.x2, param.y1, param.y2, item, count_laplace_num, param)
        else:
            for attr1 in item.square_col:
                search_square_laplace_point_num(param.x1, param.x2, param.y1, param.y2, attr1,count_laplace_num,param)
                count_num_square = count_num_square + 1
        if count_num_square % 10 == 0:
			pass
			# logging.warning("已统计区域个数为：%s" % count_num_square)

    # ？
    logging.warning("AG_CUBE----add laplace point number is:  %s" % count_laplace_num["num"])
    # 计算查询区域实际点的个数
    # act_num = search_square_actual_point_num(param.x1, param.x2, param.y1, param.y2, point_list)
    logging.warning("AG_CUBE----actual point number is:  %s" % AG_act_num)
    logging.warning("查询区域范围：x1-x2:%s-%s,y1-y2:%s-%s" % (param.x1, param.x2, param.y1, param.y2))


    return count_laplace_num["num"],AG_act_num,count

# 获取多次循环的相对误差列表
def cal_ag_cube():
	start_temp = time.time()
	starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_temp))
	logging.warning("Start loading data,  %s" % starttime)
	count, point_list = load_data("simple.txt", read_num)
	laplace_num, act_num, count = main(test_query_square,count, point_list)
	RE = cal_abs_rate(laplace_num, act_num, count)
	# AG_RE = cal_abs_rate(AG_laplace_num, AG_act_num, count)
	end_temp = time.time()
	endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_temp))
	logging.warning("共花费时间：%s" % (end_temp - start_temp))
# 带参数
def cal_ag_cube_param(param,countNum,point_list):

	laplace_num, act_num, count  = main(param,countNum,point_list)
	AG_CUBE_RE = cal_abs_rate(laplace_num, act_num, count)
	# AG_RE = cal_abs_rate(AG_laplace_num,AG_act_num,count)
	logging.warning("查询区域：x1-x2:%s-%s, y2-y2:%s-%s === AG_CUBE-相对误差为：%s" % (param.x1,param.x2,param.y1,param.y2,AG_CUBE_RE))
	return AG_CUBE_RE

if __name__ == '__main__':
	cal_ag_cube()



