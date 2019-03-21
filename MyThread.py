# coding:utf-8

import threading

class MyThred(object):

	def __init__(self,func_list=None):
		self.ret_flag = 0
		self.func_list = func_list
		self.threads = []

	def set_thred_func_list(self,func_list):
		self.func_list = func_list

	def trace_func(self,func,*args,**kwargs):
		ret = func(*args,**kwargs)
		self.ret_flag += ret3

	def start(self):
		self.threads = []
		self.ret_flag = 0
		for func_dict in self.func_list:
			if func_dict["args"]:
				t = threading.Thread(target=func_dict["func"],args=func_dict["args"])
			else:
				t = threading.Thread(target=func_dict["func"])
		for thread_obj in self.threads:
			thread_obj.start()
		for thread_obj in self.threads:
			thread_obj.join()

	def ret_value(self):
		return self.ret_flag