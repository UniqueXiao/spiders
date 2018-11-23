# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapywuyouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	position = scrapy.Field()
	salary = scrapy.Field()
	company = scrapy.Field()
	job_tag = scrapy.Field()
	job_welfare = scrapy.Field()
	#job_msg = scrapy.Field()
	#job_demands = scrapy.Field()
	
