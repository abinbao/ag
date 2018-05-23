# coding:utf-8

"""
参数配置
"""
import random
from base import Square

res_num = 10 # 循环次数

# 查询框区域
query_square = [-101, 100, -100, 100]

# 读取行数
read_num = 10000

# 阈值 e

e = 200

# 区域范围
origin_square = [360, 150]
x1_line = -(origin_square[0]/2) # x 轴边界线
x2_line = origin_square[0]/2
y1_line = -(origin_square[1]/2) # y 轴边界线
y2_line = origin_square[1]/2

random_query_square = []


# 随机获取查询区域
def get_random_square(param,set_list):
    temp_x = param[0]
    temp_y = param[1]
    x1 = random.randint(x1_line,x2_line)
    x2 = x1 + temp_x
    if x2 <= x2_line and x2 >= x1_line:
        x2 = x2
    else:
        x2 = x1
        x1 = x1-temp_x
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
example_list = {
    "6,3":None,
    "12,6":None,
    "24,12":None,
    "48,24":None,
    "96,48":None,
    "192,96":None
}

# 获取随机的查询区域列表
def get_query_square_list():
    for key in example_list:
        param = []
        set_list = set()
        param.append(int(key.split(",")[0]))
        param.append(int(key.split(",")[1]))
        for i in range(0, 100):
            get_random_square(param,set_list)
        example_list[key] = list(set_list)

if __name__ == "__main__":
    get_query_square_list()




