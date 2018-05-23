# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import numpy as np

# 拉普拉斯噪声
def laplace_noise(loc,scale,size):
	s = np.random.laplace(loc, scale, size)
	return s

# 加入拉普拉斯噪声的 区域点
def lapalce_grid_point_num(param):
    result_laplace = param + laplace_noise(0,0.1,1)[0]
    return result_laplace

# 计算相对误差
def cal_abs_rate(Q,A,Num):
    result = abs(Q-A)/max(A,0.001*Num)
    return result

if __name__ == "__main__":
    cal_abs_rate(1,1,1)