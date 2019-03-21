# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from config import get_query_square_list,test_list,pro_list
from ag_cube_v1 import cal_ag_cube,cal_ag_cube_param
# from ag_cal import cal_ag_param
from gen_log import logging
from mat_util import paint
from ag_cal_v1 import cal_ag_param
from load_data import load_data
from config import read_num
import time
import threading
def main(temp_list):
    count_points,point_list = load_data("simple.txt",read_num)

    start_temp = time.time()
    starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_temp))
    logging.warning("Start loading data,  %s" % starttime)
    result = {}
    AG_result = {}
    get_query_square_list(temp_list)
    for item in temp_list:

        RE_list = []
        RE_list_avg = []
        count = 0
        RE_AVG = 0
        for i in temp_list[item]:
            square_name = ("x1-x2:"+str(i.x1)+str(i.x2)+",y1-y2:"+str(i.y1)+str(i.y2))
            temp_squ = {}
            AG_temp_squ = {}
            # AG_RE, RE = threading.Thread(target=cal_ag_cube_param,args=(i,count_points,point_list,))
            RE = cal_ag_cube_param(i,count_points,point_list)
            temp_squ[square_name] = RE
            RE_AVG = RE_AVG + RE
            count = count + 1
            RE_list.append(temp_squ)
        # print RE_AVG
        AG_CUBE_AVG = RE_AVG/float(count+1)
        logging.warning("AG_CUBE====查询面积大小：%s，平均相对误差为：%s" % (item,AG_CUBE_AVG))
        logging.warning("=============================")
        result[item] = AG_CUBE_AVG
    # print result
    # paint(result, AG_result)
    result_ag = {}
    for item in temp_list:
        RE_list = []
        RE_list_avg = []
        RE_AVG = float(0.0)
        count = 0
        for i in temp_list[item]:
            square_name = ("x1-x2:" + str(i.x1) + str(i.x2) + ",y1-y2:" + str(i.y1) + str(i.y2))
            temp_squ = {}
            RE = cal_ag_param(i,count_points,point_list)
            logging.warning("面积大小：%s，区域：x1-%s x2-%s y1-%s y2-%s,  相对误差为：%s" % (item, i.x1, i.x2, i.y1, i.y2, RE))
            temp_squ[square_name] = RE
            RE_AVG = RE_AVG + RE
            count = count + 1
            RE_list.append(temp_squ)
        AVG = RE_AVG / float(count)
        logging.warning("面积大小：%s，平均相对误差为：%s" % (item, AVG))
        result_ag[item] = AVG
    logging.warning("ag_cube:%s" % result)
    logging.warning("ag:%s" % result_ag)
    end_temp = time.time()
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_temp))
    logging.warning("End loading data...,  %s" % endtime)
    logging.warning("共花费时间：%s" % (end_temp - start_temp))
    print result_ag
    print result
    # paint(result, AG_result)
    paint(result,result_ag)
    

if __name__ == "__main__":
    main(pro_list)