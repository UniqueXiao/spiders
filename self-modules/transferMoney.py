#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql


'''
#创建表account并插入3条数据		
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='test', charset='utf8')
#关闭自动提交
conn.autocommit(False)
cursor = conn.cursor()
sql_createTb = """CREATE TABLE account(
				id INT NOT NULL AUTO_INCREMENT,
				name CHAR(20),
				password CHAR(20),
				money INT,
				PRIMARY KEY(id))
	       """
sql_insert = """INSERT INTO account(name, password, money) 
				VALUES
				('xx', '123', 200),
				('yy', '456', 500),
				('zz', '789', 20)
			"""
try:
	cursor.execute(sql_createTb)
	cursor.execute(sql_insert)
	conn.commit()
except Exception as e:
	print('Reason:', e)
	conn.rollback()
finally:
	cursor.close()
	conn.close()
'''




class TransferMoney(object):
	def __init__(self, conn):
		self.conn = conn
		
	def transfer(self, sourceID, targetID, money):
		#其他函数中若有错会抛出异常而被检测到
		try:
			self.checkIdAvailable(sourceID)
			self.checkIdAvailable(targetID)
			self.ifEnoughMoney(sourceID, money)
			self.reduceMoney(sourceID, money)
			self.addMoney(targetID, money)
			self.conn.commit()
		except Exception as e:
			self.conn.rollback()
			raise e
			
	def checkIdAvailable(self, ID):
		cursor = self.conn.cursor()
		try:
			sql = "select * from account where id = %d" %(ID)
			cursor.execute(sql)
			rs = cursor.fetchall()
			if len(rs) != 1:
				raise Exception("账号 %d 不存在！" %(ID))
		finally:
			cursor.close()
			
	def ifEnoughMoney(self, ID, money):
		cursor = self.conn.cursor()
		try:
			sql = "select * from account where id = %d and money >= %d" %(ID, money)
			cursor.execute(sql)
			rs = cursor.fetchall()
			if len(rs) != 1:
				raise Exception("账号 %d 不足 %d Yuan!" %(ID, money))
		finally:
			cursor.close()
			
	def reduceMoney(self, ID, money):
		cursor = self.conn.cursor()
		try:
			sql = "update account set money = money - %d where id = %d" %(money, ID)
			cursor.execute(sql)
			if cursor.rowcount != 1:
				raise Exception("扣款失败！")
		finally:
			cursor.close()
		 
	def addMoney(self, ID, money):
		cursor = self.conn.cursor()
		try:
			sql = "update account set money = money + %d where id = %d" %(money, ID)
			cursor.execute(sql)
			if cursor.rowcount != 1:
				raise Exception("加款失败！")
		finally:
			cursor.close()
			

if __name__ == '__main__':
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='test', charset='utf8')
	trMoney = TransferMoney(conn)
	sourceID = 3
	targetID = 5
	money = 50
	
	try:
		trMoney.transfer(sourceID, targetID, money)
	except Exception as e:
		print('出现问题:'+str(e))
	finally:
		conn.close()
			


