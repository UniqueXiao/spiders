# -*- coding: utf-8 -*-
import scrapy
from scrapyWuyou.items import ScrapywuyouItem
import time
from selenium import webdriver
option = webdriver.ChromeOptions()
option.add_argument('headless')   # 不弹出浏览器窗口


class WuyouSpider(scrapy.Spider):
	name = 'wuyou'
	allowed_domains = ['www.51job.com']
	base_url = 'http://www.51job.com/'
	visited_page_urls = set()    #存放已爬取过的列表页
	visited_detail_urls = set()  #存放已爬取过的详情页
	#new_urls = set()
    #start_urls = ['http://www.51job.com/']
	
	def start_requests(self):
		kwd = self.settings.get('KEYWORDS')[0]   #搜索关键词，定义在settings.py中
		driver = webdriver.Chrome(chrome_options=option)
		driver.get(self.base_url)
		time.sleep(1)
		driver.find_element_by_id('kwdselectid').clear()
		time.sleep(0.2)
		driver.find_element_by_id('kwdselectid').send_keys(kwd)
		time.sleep(0.5)
		driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/button').click()
		
		jumped_url = driver.current_url
		driver.quit()
		yield scrapy.Request(url=jumped_url, callback=self.parse)
		

	def parse(self, response):
		
		for div in response.xpath('//div[@id="resultList"]/div[contains(@class, "el")]')[1:]:
			url = div.xpath('p/span/a/@href').extract()[0]    # 详情页链接
			if url not in self.visited_detail_urls:
				self.visited_detail_urls.add(url)
				yield scrapy.Request(url=url, callback=self.parse_detail, dont_filter=True)
			
		for link in response.xpath('//div[@class="dw_page"]/div/div/div/ul/li/a/@href').extract():
			if link not in self.visited_page_urls:           # 翻页链接
				self.visited_page_urls.add(link)
				yield scrapy.Request(url=link, callback=self.parse, dont_filter=True)

	def parse_detail(self, response):    # 解析详情页
		item = ScrapywuyouItem()
		item['position'] = response.xpath('//h1/text()').extract()[0].strip()
		item['salary'] = response.xpath('//div[@class="cn"]/strong/text()').extract()[0].strip()
		item['company'] = response.xpath('//div[@class="cn"]/p[@class="cname"]/a[1]/text()').extract()[0].strip()
		item['job_tag'] = ';'.join(response.xpath('//div[@class="cn"]/p[@class="msg ltype"]/text()').extract()).strip().replace('\xa0', '')
		item['job_welfare'] = ';'.join(response.xpath('//div[@class="jtag"]/div[@class="t1"]/span/text()').extract())
		
		yield item
		