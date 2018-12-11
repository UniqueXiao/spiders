#!/usr/bin/env python3

import asyncio
import aiohttp
import requests
from lxml import etree
import re
import time
import pandas as pd


root_url = 'https://www.aihuishou.com'
target_url = '/shouji?all=True'
headers = headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3381.1 Safari/537.36'}

names = []
prices = []
visited_urls = set()

async def fetch(session, url):
	async with session.get(url, headers=headers) as response:
		return await response.text()
	

async def parse(res):
	global names, prices

	html = etree.HTML(res)
	name_list = html.xpath('//div[@class="product-list-wrapper"]/ul/li/a/p/text()')
	price_list = []
	comment_list = html.xpath('//div[@class="product-list-wrapper"]/ul/li/a/comment()')
	for comment in comment_list:
		price = re.findall('\d+', str(comment))[0]
		price_list.append(price)
		
	names += name_list
	prices += price_list
	
		
def get_next_page():
	cur_url = root_url + target_url
	while cur_url not in visited_urls:
		visited_urls.add(cur_url)
		res = requests.get(cur_url, headers=headers)
		html = etree.HTML(res.text)
		next_page = html.xpath('//div[@class="product-list-pager"]/a/@href')[-1]
		yield cur_url
		cur_url = root_url + next_page
		

async def download(url):
	async with aiohttp.ClientSession() as session:
		res = await fetch(session, url)
		await parse(res)

start = time.time()
		
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(download(url)) for url in get_next_page()]
tasks = asyncio.gather(*tasks)
loop.run_until_complete(tasks)

df = pd.DataFrame({'name': names, 'price': prices})
df.to_csv(r'C:\Users\Administrator\Desktop\123.csv', encoding='utf-8', index=False)
print(time.time() - start)