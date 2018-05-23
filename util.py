# coding:utf-8
"""
@desc 工具类
"""

from base import Point,Square,Line_x,Line_y
import math
from laplace import lapalce_grid_point_num,laplace_noise
from gen_log import logging
from config import res_num,read_num,query_square,e

# 生成 x 轴的分割线
def genrate_line_x(param):
	x1 = param.x1
	x2 = param.x2
	y1 = param.y1
	y2 = param.y2
	# 参数 N a e c
	m2 = cal_grid_m2(float(param.count), 0.5, 0.1, 5)
	if m2 == 0:
		return
	x_unit = float(x2 - x1) / float(m2)
	x_bottom = x1
	for i in range(0,int(m2)-1):
		line_x = Line_x(x_bottom+x_unit,y1,y2)
		param.line_x_list.append(line_x)
		x_bottom = x_bottom+x_unit


# 生成 y 轴的分割线
def genrate_line_y(param):
	x1 = param.x1
	x2 = param.x2
	y1 = param.y1
	y2 = param.y2
	# 参数 N a e c
	m2 = cal_grid_m2(float(param.count), 0.5, 0.1, 5)
	if m2 == 0:
		return
	y_unit = float(y2 - y1) / float(m2)

	y_bottom = y1
	for i in range(0, int(m2) - 1):
		line_y = Line_y(x1, x2, y_bottom+y_unit)
		param.line_y_list.append(line_y)
		y_bottom = y_bottom + y_unit


# 统计 m1 的 共分 m1*m1 个网格
def cal_grid_num(n,e,c):

	m = max(10,math.ceil(0.25*math.sqrt((n*e)/c)))

	return m

# 统计 m2 共分 m2*m2 个网格
def cal_grid_m2(N,a,e,c):
	m2 = math.ceil(math.sqrt(N*(1-a)*e/c))
	return m2



"""
@desc:第一次 划分网格
@:param square_list 区域集合
		num 点集合的个数
		x y  坐标范围
"""
def divide_grid(square_list,num,x,y):

	x_unit = float(x)/float(num) # 横坐标单元格宽度
	y_unit = float(y)/float(num) # 纵坐标单元长度

	y_bottom = -(y/2)
	x_bottom = -(x/2)
	for i in range(0,num):
		temp = y_bottom
		for i in range(0,num):
			square = Square(x_bottom,float('%.2f' % (x_bottom + x_unit))
							,temp,temp+y_unit,0)
			temp = temp+y_unit
			square_list.append(square)
		x_bottom = float('%.2f' % (x_bottom + x_unit))
	return square_list

"""
统计每个区域 点的个数

@:param square_list 区域集合
		point_list 点的集合
"""
def cal_point_num(square_list,point_list):
	for item in square_list:
		for j in point_list:
			if j.x >= item.x1 and j.x <= item.x2 and j.y >= item.y1 and j.y <= item.y2:
				item.count = item.count + 1
		item.count_laplace = lapalce_grid_point_num(item.count)

"""
第二次划分网格

@:param item 区域类
"""

def divide_grid2(item):
	x1 = item.x1
	x2 = item.x2
	y1 = item.y1
	y2 = item.y2
	# 参数 N a e c
	m2 = cal_grid_m2(float(item.count),0.5,0.1,5)
	if m2 == 0:
		pass
	else:
		x_unit = float(x2-x1)/float(m2)
		y_unit = float(y2-y1)/float(m2)

		x_bottom = x1
		y_bottom = y1
		for i in range(0, int(m2)):
			temp = y_bottom
			for i in range(0, int(m2)):
				square = Square(x_bottom, float('%.2f' % (x_bottom + x_unit))
								, temp, temp + y_unit, 0)
				temp = temp + y_unit
				item.square_col.append(square)
			x_bottom = float('%.2f' % (x_bottom + x_unit))
		# 计算区域中 子区域的点的平均个数
		item.avg = float(item.count)/float(len(item.square_col))

"""
计算 H 判断区域是否需要划分
@:param a 阈值
"""
def cal_valueOfH(a,param):

	temp = 0.0
	for item in param.square_col:
		temp = temp + abs(float(item.count)-float(param.avg))
	# 如果区域的 H 值小于 给定的阈值 a, 那么就不需要再进行分割 flag = False (默认为False)
	# 如果区域的 H 值大于 给定的阈值 a, 那么就继续分割 flag = True
	if temp > a:
		param.flag = True

"""
计算最适合的分割线
@:param param 区域范围
"""
def find_gold_line(param,point_list):

	if len(param.line_x_list) == 0 or len(param.line_y_list) == 0:
		pass
	else:
		x_gold_line = param.line_x_list[0]
		y_gold_line = param.line_y_list[0]
		x_value = cal_square_x(x_gold_line,param,point_list)
		y_value = cal_square_y(y_gold_line,param,point_list)

		for i in range(1,len(param.line_x_list)):
			temp_value = cal_square_x(i,param,point_list)
			if temp_value < x_value:
				x_gold_line = i
				x_value = temp_value

		for i in range(1,len(param.line_y_list)):
			temp_value = cal_square_y(i,param,point_list)
			if temp_value < y_value:
				y_gold_line = i
				y_value = temp_value
		if x_value <= y_value:
			param.gold_line = x_gold_line
			squareD1 = Square(param.x1,x_gold_line.x1,param.y1,param.y2,0)
			squareD2 = Square(x_gold_line.x1,param.x2,param.y1,param.y2,0)
			param.square_D1 = squareD1
			param.square_D2 = squareD2
		else:
			param.gold_line = y_gold_line
			squareD1 = Square(param.x1,param.x2,param,y1,y_gold_line.y1,0)
			squareD2 = Square(param.x1,param.x2,y_gold_line.y1,param.y2,0)
			param.square_D1 = squareD1
			param.square_D2 = squareD2

"""
计算分割区域的 v1 v2 n1 n2
@:param line x 轴分割线
		square 区域
		point_list 点集合
"""
# 遍历 x 线

def cal_square_x(line,square,point_list):

	points_D1 = 0 # D1 区域中点的个数 v1
	points_D2 = 0 # D2 区域中点的个数 v2

	squares_D1 = 0 # D1 中划分的区域的个数 n1
	squares_D2 = 0 # D2 中划分的区域的个数 n2

	for point in point_list:
		if point.x >= square.x1 and point.x <= line.x1 and point.y >= square.y1 and point.y <= square.y2:
			points_D1 = points_D1 + 1
	points_D2 = square.count - points_D1

	for item in square.square_col:
		if item.x2 <= line.x1 and item.x1 >= square.x1 and item.y1 >= square.y1 and item.y2 <= square.y2:
			squares_D1 = squares_D1 + 1

	squares_D2 = len(square.square_col) - square.square_col

	value = points_D1*squares_D1 + points_D2*squares_D2

	return value

# 遍历 y 线

def cal_square_y(line,square,point_list):

	points_D1 = 0  # D1 区域中点的个数 v1
	points_D2 = 0  # D2 区域中点的个数 v2

	squares_D1 = 0  # D1 中划分的区域的个数 n1
	squares_D2 = 0  # D2 中划分的区域的个数 n2

	for point in point_list:
		if point.y1 >= square.y1 and point.y1 <= line.y1 and point.x1 >= square.x1 and point.x2 <= square.x2:
			points_D1 = points_D1 + 1
	points_D2 = square.count - points_D1

	for item in square.square_col:
		if item.x1 >= square.x1 and item.x2 <= square.x2 and item.y1 >= square.y1 and item.y2 <= line.y1:
			squares_D1 = squares_D1 + 1

	squares_D2 = len(square.square_col) - square.square_col

	value = points_D1*squares_D1 + points_D2*squares_D2

	return value

"""
遍历 and 合并 
@:param param 划分区域
"""
def recursion_merge(param,point_list):

    divide_grid2(param)
    cal_point_num(param.square_col, point_list)
    genrate_line_x(param)
    genrate_line_y(param)
    cal_valueOfH(e, param)

    # 如果 flag = True, 对该区域继续分割, 并找出最分割最平均的分割线
    if param.flag:
        find_gold_line(param, point_list)
        recursion_merge(param.square_D1, point_list)
        recursion_merge(param.square_D2, point_list)
    else:
		param.square_col = None

"""
递归打印
"""
def recursion_print(square_list):
    for item in square_list:
        if len(item.square_col) != 0:
		    print "子区域个数为：%s" % len(item.square_col)
		    recursion_print(item.square_col)


# 查询区域 laplace噪声  个数
"""
x1 x2 y1 y2 查询区域
result_laplace 加入拉普拉斯噪声的各个区域中包含点的个数
"""
def search_square_laplace_point_num(x1,x2,y1,y2,item,count):

	if(item.flag == False):
		x3 = float(item.x1)
		x4 = float(item.x2)
		y3 = float(item.y1)
		y4 = float(item.y2)
		# 区域面积
		square = (x4-x3)*(y4-y3)
		# 1. 全部在区域中
		if x3 >=x1 and x4<=x2 and y3>=y1 and y4 <= y2:
			count["num"] = count["num"] + item.count_laplace
		# 2. 左上角
		elif x3 <=x1 and x4 >=x1 and x4 <=x2 and y3 >= y1 and y3 <=y2 and y4 >=y2:
			rate = (x4-x1)*(y2-y3)/square
			count["num"] = count["num"] + item.count_laplace*rate
		# 3. 左边
		elif x3 <= x1 and x4 >= x1 and x4 <= x2 and y3 >= y1 and y4 <=y2:
			rate = (x4-x1)*(y4-y3)/square
			count["num"] = count["num"] + item.count_laplace*rate
		# 4. 左下角
		elif x3 <= x1 and x4 >= x1 and x4 <=x2 and y3 <=y1 and y4 >= y1 and y4 <= y2:
			rate = (x4-x1)*(y4-y1)/square
			count["num"] = count["num"] + item.count_laplace*rate
		# 5. 下边
		elif x3 >= x1 and x4 <= x2 and y3 <= y1 and y4 >=y1 and y4 <= y2:
			rate = (x4-x3)*(y4-y1)/square
			count["num"] = count["num"] + item.count_laplace*rate
		# 6. 右下角
		elif x3 >= x1 and x3 <= x2 and x4 >= x2 and y3 <= y1 and y4 >= y1 and y4 <= y2:
			rate = (x2-x3)*(y4-y1)/suqare
			count["num"] = count["num"] + item.count_laplace*rate
		# 7. 右边
		elif x3 >= x1 and x3 <= x2 and x4 >= x2 and y3>= y1 and y4 <= y2:
			rate = (x2-x3)*(y4-y3)/square
			count["num"] = count["num"] + item.count_laplace*rate
		# 8. 右上角
		elif x3 >= x1 and x3 <= x2 and x4 >= x2 and y3>=y1 and y3 <= y2 and y4 >= y2:
			rate = (x2-x3)*(y2-y3)/square
			count["num"] = count["num"] + item.count_laplace*rate
		# 9. 上边
		elif x3 >= x1 and x4 <= x2 and y3>=y1 and y3 <=y2 and y4 >= y2:
			rate = (x4-x3)*(y2-y3)/square
			count["num"] = count["num"] + item.count_laplace*rate

	else:
		for ii in item.square_col:
			search_square_laplace_point_num(query_square[0], query_square[1], query_square[2], query_square[3], ii, count)

# 查询区域 实际 个数
def search_square_actual_point_num(x1,x2,y1,y2,point_list):
	count = 0
	for item in point_list:
		x_loc = item.x
		y_loc = item.y
		if x_loc >=x1 and x_loc <=x2 and y_loc >= y1 and y_loc <= y2:
			count  = count + 1
	if count%10000 == 0:
		logging.warning("实际统计数量：%s" % count)
	return count

def main():
	pass
if __name__ == "__main__":
	main()