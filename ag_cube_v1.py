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
from config import read_num,query_square,res_num,origin_square,e

# 主函数
def main():

	# 加载经纬度集合 count:加载点的个数  point_list:点的集合
    count,point_list = load_data("simple.txt",read_num)

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

	# 计算 H 判断区域是否需要继续划分
    for attr1 in square_list:
		for attr2 in attr1.square_col:
			# 划分网格
			if len(attr2.square_col) == 0:
				continue
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
            count_num_square = count_num_square + 1
        else:
            for attr1 in item.square_col:
                search_square_laplace_point_num(query_square[0], query_square[1], query_square[2], query_square[3], attr1,count_laplace_num)
                count_num_square = count_num_square + 1
        if count_num_square % 10 == 0:
			logging.warning("已统计区域个数为：%s" % count_num_square)

    # ？
    logging.warning("拉普拉斯-查询区域点个数：%s" % count_laplace_num["num"])
    # 计算查询区域实际点的个数
    act_num = search_square_actual_point_num(query_square[0], query_square[1], query_square[2], query_square[3], point_list)
    logging.warning("实际-查询区域点个数：%s" % act_num)

    return count_laplace_num["num"],act_num,count

def cal_ag_cube():
	start_temp = time.time()
	starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_temp))
	logging.warning("Start loading data,  %s" % starttime)
	result = []
	for i in range(0, res_num):
		laplace_num, act_num, count = main()
		RE = cal_abs_rate(laplace_num, act_num, count)
		write_data("ag_cube_result.txt", RE)
		result.append(RE)
		logging.warning("第 %s 次运行 函数：AG_CUBE." % (i+1))
	end_temp = time.time()
	endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_temp))
	logging.warning("共花费时间：%s" % (end_temp - start_temp))
	return result

if __name__ == '__main__':
	cal_ag_cube()



