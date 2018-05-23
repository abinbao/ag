# coding:utf-8
"""
@author:xiaobin
@desc: ag_cube
@date: 2018-05-14
"""

import sys
reload(sys)
import time
sys.setdefaultencoding("utf-8")

# 点类 x y 分别对应 经纬线
class Point(object):

	def __init__(self,x,y):
		self.x = x # x 坐标
		self.y = y # y 坐标

# 区域类 四个点确定一个区域
class Square(object):

	def __init__(self,x1,x2,y1,y2,count):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.count = count # 区域中点的个数
		self.count_laplace = 0 # 加入噪声的点的个数
		self.avg = 0 # 子区域平均点的个数
		self.square_col = [] # 分割的区域集合
		self.line_x_list = [] # 存储区域的 x 轴的分割线
		self.line_y_list = [] # 存储区域的 y 轴的分割线
		self.gold_line = None # 黄金分割线
		self.flag = False # 判断是否需要分割 默认为false 不需要分割
		self.square_D1 = None # 黄金分割 D1 区域
		self.square_D2 = None  # 黄金分割 D2 区域

	def system_out(self):
		print "区域 x 轴范围为：%s - %s ，y 轴范围为：%s - %s ." % (self.x1,self.x2,self.y1,self.y2)
		print "区域内个数为：%s" % self.count
		print "区域内-二次划分区域个数：%s" % len(self.square_col)

	def print_avg(self):
		print "区域点的平均个数为：%s" % (self.avg)
	def print_count(self):
		print "区域点的个数为：%s" % (self.count)
	def print_flag(self):
		print "区域是否需要继续划分：%s" % self.flag
	# 重写 set 判重机制
	def __eq__(self, other):
		if isinstance(other,Square):
			return ((self.x1 == other.x1) and (self.x2 == other.x2) and (self.y1 == other.y1) and (self.y2 == other.y2) and (self.count == other.count))
		else:
			return False
	def __ne__(self,other):
		return (not self.__eq__(other))
	def __hash__(self):
		return hash(self.x1) + hash(self.x2) + hash(self.y1) + hash(self.y2)

# y 轴分割线
class Line_y(object):

	def __init__(self,x1,x2,y1):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1

	def system_out(self):
		print "线的 x1-x2 ：%s - %s , y 坐标为：%s" % (self.x1,self.x2,self.y1)
# x 轴分割线
class Line_x(object):

	def __init__(self,x1,y1,y2):
		self.x1 = x1
		self.y1 = y1
		self.y2 = y2

	def system_out(self):
		print "线的 y1-y2 ：%s - %s , x 坐标为：%s" % (self.y1,self.y2,self.x1)