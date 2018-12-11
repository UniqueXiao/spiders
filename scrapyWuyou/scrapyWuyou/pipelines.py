# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi   # 通过pymysql+twisted异步保存到MySQL
import logging
logger = logging.getLogger(__name__)

class ScrapywuyouPipeline(object):
	def __init__(self, dbpool):
		self.dbpool = dbpool
		
	@classmethod
	def from_settings(cls, settings):
		# 获取settings中的配置信息
		dbparams = dict(
			host = settings['MYSQL_HOST'],
			port = settings['MYSQL_PORT'],
			db = settings['MYSQL_DB'],
			user = settings['MYSQL_USER'],
			passwd = settings['MYSQL_PASSWORD'],
			charset = settings['MYSQL_CHARSET'],
			cursorclass = pymysql.cursors.DictCursor,
			use_unicode = False,
		)
		
		# **表示将字典扩展为关键字参数,相当于host=xxx, db=yyy.....
		dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
		return cls(dbpool)

	def process_item(self, item, spider):
		# 使用twisted将mysql插入变成异步执行
		query = self.dbpool.runInteraction(self._conditional_insert, item)   # 调用插入数据的方法
		query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
		return item
		
	def _conditional_insert(self, cursor, item):
		# 执行具体的插入
		# print(item['position'])
		sql = "INSERT INTO wuyou_test (position, salary, company, job_tag, job_welfare, job_category, job_msg) VALUES (%s, %s, %s, %s, %s, %s, %s)"
		params = (item['position'], item['salary'], item['company'], item['job_tag'], item['job_welfare'], item['job_category'], item['job_msg'])
		cursor.execute(sql, params)

	def _handle_error(self, failue, item, spider):
		# 处理异步插入的异常
		#print(failue)
		logger.error(item['url'])
