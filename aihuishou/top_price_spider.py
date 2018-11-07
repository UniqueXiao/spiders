import requests
from lxml import etree
import re
import pandas as pd
import datetime

date = datetime.datetime.now().strftime('%Y%m%d')   #获取当前日期


root_url = 'https://www.aihuishou.com'

phone_url = '/shouji?all=True'   #手机url
pad_url = '/pingban?all=True'    #平板url
laptop_url = '/laptop?all=True'  #笔记本url

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3381.1 Safari/537.36'}


def parse_page(url):

	#names = []
	prices = []
	
	n = 1  #记录循环次数
	
	r = requests.get(url, headers=headers)
	html = etree.HTML(r.text)
	names = html.xpath('//div[@class="product-list-wrapper"]/ul/li/a/p/text()')
	comments = html.xpath('//div[@class="product-list-wrapper"]/ul/li/a/comment()')
	
	for comment in comments:
		price = re.findall('\d+', str(comment))[0]
		
		if price == '0':    #如果注释中价格为0，则进入产品页抓取最高价
			p_url = str(html.xpath('//*[@id="body"]/div[4]/ul/li[%d]/a/@href' %(n))[0])
			price = parse_product_page(root_url+p_url)
			prices.append(price)
		else:
			prices.append(price)
			
		n += 1
	
	return names,prices


def get_pages(url):
	
	n = 0
	pages = [url,]
	
	while n < 999:
		r = requests.get(root_url+pages[n],headers=headers)
		html = etree.HTML(r.text)
		next_page_url = html.xpath('//div[@class="product-list-pager"]/a/@href')[-1]
		
		if next_page_url not in pages:
			pages.append(next_page_url)
		else:
			break
			
		n += 1
	#print(n)
	
	return pages


def parse_product_page(url):
	
	r = requests.get(url, headers=headers)
	
	if r.status_code == 200:
		html = etree.HTML(r.text)
		if len(html.xpath('//*[@id="group-property"]/div[1]/ul/li')) == 2:
			price = html.xpath('//*[@id="group-property"]/div[1]/ul/li[2]/text()')[0].replace('\n', '').replace(' ', '')
		else:
			price = '无报价'
	else:
		print(r'----------请求失败，状态码为%s----------' % (str(r.status_code)))
		return None
	
	return price
	
	
def main(url):
	
	p_name = []
	p_price = []
	i = 1
	
	for page_url in get_pages(url):
		try:
			names,prices = parse_page(root_url+page_url)
			p_name += names
			p_price += prices
			print(r'------------第%s页数据已抓取完毕!!!------------' %(str(i)))
		except:
			print(r'------------第%s页数据抓取失败!!!!!------------' %(str(i)))
			
		i += 1

	print(r'------------数据已全部抓取完毕!!!!!------------')
	
	return p_name, p_price
	
	
	
if __name__ == '__main__':
	p_name, p_price = main(phone_url)
	df = pd.DataFrame({'p_name': p_name, 'p_price': p_price})
	#print(df)
	df.to_csv(r'C:\Users\Administrator\Desktop\phone_price%s.csv' %(date), encoding='utf-8', index=False)



