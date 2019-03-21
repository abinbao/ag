# coding:utf-8

"""
参数配置
"""
import random
from base import Square

res_num = 10 # 循环次数

# 查询框区域
test_query_square = Square(-102, -96, 28, 31,0)

# 读取行数
read_num = 10000

# 阈值 e

e = 20

# 区域范围
origin_square = [360, 150]
x1_line = -(origin_square[0]/2) # x 轴边界线
x2_line = origin_square[0]/2
y1_line = -(origin_square[1]/2) # y 轴边界线
y2_line = origin_square[1]/2

random_query_square = []


# 随机生成查询区域
"""
@:param param 对应的查询区域的 长和宽
        set_list 存储不相同的查询区域
"""
def get_random_square(param,set_list):

    temp_x = param[0] # x 轴的间距
    temp_y = param[1] # y 轴的间距
    x1 = random.randint(x1_line,x2_line) # x1_line 是大区域的左边界，x2 是大区域的右边界 ，随机在其中取一点为x1
    x2 = x1 + temp_x # x2 即为 x1 加上 x 轴的间距
    # 判断 x2 是否超出了大区域的范围 ，如果没有超过，那么查询区域的x轴范围确定为 x1 到 x2
    # 如果 超过了，那么查询区域的 x 轴范围 就为 x1-temp_x 到 x1
    if x2 <= x2_line and x2 >= x1_line:
        x2 = x2
    else:
        x2 = x1
        x1 = x1-temp_x
    # y 轴 同理 x 轴
    y1 = random.randint(y1_line,y2_line)
    y2 = y1 + temp_y
    if y2 <= y2_line and y2 >= y1_line:
        y2 = y2
    else:
        y2 = y1
        y1 = y1 - temp_y
    square = Square(x1,x2,y1,y2,0)
    set_list.add(square)

# 查询区域面积
pro_list = {
    "6,3":None,
    "12,6":None,
    "24,12":None,
    "48,24":None,
    "96,48":None,
    "192,96":None
}

# 测试集
test_list = {
    "6,3":None
}


# 获取随机的查询区域列表
"""
@:param example_list 查询区域的 长和宽列表
"""
def get_query_square_list(example_list):
    # 遍历列表
    for key in example_list:
        param = []
        # 因为不能存储相同的区域 所以是用 set() 集合
        set_list = set()
        param.append(int(key.split(",")[0]))
        param.append(int(key.split(",")[1]))
        # 遍历循环 固定长和宽 下的查询区域 n 次
        for i in range(0, 2):
            get_random_square(param,set_list)
        example_list[key] = list(set_list)
if __name__ == "__main__":
    get_query_square_list(test_list)




