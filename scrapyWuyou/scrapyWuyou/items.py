# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import TakeFirst


def lst_convert_str(lst):
	try:
		res = ';'.join(lst).strip().replace('\t', '').replace('\r', '').replace('\n', '').replace('\xa0','')
	except:
		res = lst
		
	return res

class ScrapywuyouItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	position = scrapy.Field(
		input_processor = lst_convert_str,
		output_processor= TakeFirst()
    )
	salary = scrapy.Field(
		input_processor = lst_convert_str,
		output_processor= TakeFirst()
	)
	company = scrapy.Field(
		input_processor = lst_convert_str,
		output_processor= TakeFirst()
	)
	job_tag = scrapy.Field(
		input_processor = lst_convert_str,
		output_processor= TakeFirst()
	)
	job_welfare = scrapy.Field(
		input_processor = lst_convert_str,
		output_processor= TakeFirst()
	)
	job_category = scrapy.Field(
		input_processor = lst_convert_str,
		output_processor= TakeFirst()
	)
	job_msg = scrapy.Field(
		input_processor = lst_convert_str,
		output_processor= TakeFirst()
	)
	url = scrapy.Field(
		output_processor = TakeFirst()
	)
