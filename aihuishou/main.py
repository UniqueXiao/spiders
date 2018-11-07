#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import json
import time
from id_units_generator import get_ids_all


root_url = 'https://www.aihuishou.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3381.1 Safari/537.36'}



def get_id_values(url):                      #获取id对应的具体选项

	r = requests.get(url, headers=headers)
	
	if r.status_code == 200:
	
		id_values = {}
		
		html = etree.HTML(r.text)
		if html.xpath('//div[@class="select-property base-property"]'):
			dls = html.xpath('//div[@class="select-property base-property"]/dl')
			for dl in dls:
				lis = dl.xpath('./dd/ul/li')
				for li in lis:
					id = li.xpath('./@data-id')[0]
					value = li.xpath('./div/text()')[0]
					id_values[id] = value
			
		if html.xpath('//div[@class="select-property appearance-property deactive"]'):
			dls = html.xpath('//div[@class="select-property appearance-property deactive"]/dl')
			for dl in dls:
				lis = dl.xpath('./dd/ul/li')
				for li in lis:
					id = li.xpath('./@data-id')[0]
					value = li.xpath('./div/text()')[0]
					id_values[id] = value
				
		if html.xpath('//div[@class="select-property function-property deactive"]'):
			dls = html.xpath('//div[@class="select-property function-property deactive"]/dl')
			for dl in dls:
				lis = dl.xpath('./dd/ul/li')
				for li in lis:
					id = li.xpath('./@data-id')[0]
					value = li.xpath('./span')[1].xpath('./text()')[0]
					id_values[id] = value
				
		return id_values
		
	else:
		print(r.status_code)
		return None



			
def get_key(pid, price_unit, mid=''):        #获取重定向链接中的url

	create_url = 'https://www.aihuishou.com/userinquiry/create'
	
	headers1 = {
            'Host': 'www.aihuishou.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': '*/*',
            'Origin': 'http://www.aihuishou.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://www.aihuishou.com/product/%s.html?priceValues=%s'%(pid,price_unit),
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'gr_user_id=321ad088-a906-4507-b80f-f3b0ce365b20; _uab_collina=152698294188997761284568; _ga=GA1.2.704543447.1526982943; NTKF_T2D_CLIENTID=guestD4227123-29E6-C635-C1C8-8746A9AFA35B; __sonar=6540205825241581962; Hm_lvt_d967f933b496a0741b57f403503a1d89=1527042858,1527126507,1527132370,1527139760; _jzqa=1.989326390967560700.1526982945.1531803972.1531811048.216; _jzqx=1.1526982945.1531811048.108.jzqsr=aihuishou%2Ecom|jzqct=/.jzqsr=aihuishou%2Ecom|jzqct=/product/17462%2Ehtml; _qzja=1.736562044.1526982945246.1531803972122.1531811047665.1531813492684.1531813513021.0.0.0.4268.215; acw_tc=AQAAADTv3lXH1gkAClJYcQ+Lv54BMiDf; Hm_lvt_6206c0fb3ed4e6feb904c97664c91527=1531793496,1531877601,1531962864,1532049463; _pk_ref.1.5e06=%5B%22%22%2C%22%22%2C1532063906%2C%22http%3A%2F%2Fgo.17taotaoba.com%2F%3Fid%3Dbdd5495VKj6NFxVP3ZAdTyrsEilSmfnxllRV0xPkm6zNWMjBDypyXxghyj5%22%5D; _pk_ses.1.5e06=*; portal_city=1; portal_city_default=1; .NetCoreSession_Portal=CfDJ8P4lRpsSt1FEoqTwobrkvZIppX2iaS4qMrjDdOCz638U4p0uByxJBK6EnhqE8TPUlT48PoVkNzZAw1D%2B804HOo96wnS0U4%2FDsgx8%2BAEl0LrGpKaQivjozEFp3PgT7DUiHQw6pY6FG59qhKDZbBaN8sHSsDxOIJDv8K9be%2BVaSZnb; _umdata=BA335E4DD2FD504F1AC98890EF3759CCB70A71F03DF0956F53FBEBA9DE1854F2558954228AE2E8D4CD43AD3E795C914CBBDA98A5B73DEE95C1C0FCFE50BA9AE5; portal_cart=%5B%7B%22InquiryKey%22%3A%225935801852735701136%22%2C%22Checked%22%3Afalse%2C%22AfreshFail%22%3Afalse%7D%5D; gr_session_id_b053e784452fb69e=d4129ed1-65dd-4a97-9d50-4aad6d8f747e; gr_session_id_b053e784452fb69e_d4129ed1-65dd-4a97-9d50-4aad6d8f747e=true; nTalk_CACHE_DATA={uid:kf_9741_ISME9754_guestD4227123-29E6-C6,tid:1532076056061524}; u_asec=099%23KAFEaEEKE5YEhGTLEEEEEpEQz0yFD6DFSXyMV6tcScR4W6thSrRYn6PTZf7TEEiStEE7BYFETEEEbORuE7EFNIaHFoMTEpQEGyKs%2FqYWcR4f9BZLDRbBbRiqwsnc6RXWHQe6r0MQcyoCwQeYLA8yhKLu3yaIPL29cFQqPtIObw2W1QszZVUy8AylGc9xHg4MhiutVPM28gM0%2FLlLaA8MhT8t3rBmhgM08RQluqeMhTGk3%2FsNSjM08KLE%2FXyBh0Ukh9QusoF08K42%2FBsNSAGScLOcLrsTNsrsraSp%2FfkWPR4SL7lW8yXZNa%2Bp9yniqOIdHda3rfBrE7Eht%2FMFE6rpBEFE13iSEIDykvJfsEFEp3iSlllP%2F3iSt37MlXZdtSRStTLtsyaGC3iSh3nP%2F3wYt37MlXZddcwUE7TxGHy9D5GbvFt0DLLgBwu6iMSqqXSGq7rfZDz%2FtiEsZHLokx%2Fgcv60JmZo09m4k4GcmStrLLIZmGP0DLOvBwD0D4Gcm%2FN4k4AqmStrLLFCmGP0D4MTEEySt9llsyG%3D; _pk_id.1.5e06=6c34f64b814a8016.1526982945.228.1532076919.1532056918.; Hm_lpvt_6206c0fb3ed4e6feb904c97664c91527=1532076919'
        }
	
	data = {
		'AuctionProductId': pid,
		'ProductModelId':  mid,
		'PriceUnits': price_unit,
	}
	
	r = requests.post(create_url, data=data, headers=headers1)
	if r.status_code == 200:
		
		key_obj = json.loads(r.text)
		try:
			if 'code' in key_obj.keys():
				if key_obj['code'] == 3001:
				
					cha_url = key_obj['data']['captchaUrl']
					print(key_obj['data']['captchaUrl'])
					save_pic(cha_url)
					ver_code = input('请输入验证码:')
					data = {
						'AuctionProductId': pid,
						'ProductModelId': mid,
						'PriceUnits': price_unit,
						'imgCaptcha': ver_code
					}
					r = requests.post(create_url, data=data, headers=headers1)
					key_obj = json.loads(r.text)
						
					while key_obj['code'] == 3002:
						print('--------------------验证码输入错误--------------------')
						#time.sleep(1)
						cha_url = key_obj['data']['captchaUrl']
						print(key_obj['data']['captchaUrl'])
						save_pic(cha_url)
						ver_code = input('请重新输入验证码:')
						data = {
							'AuctionProductId': pid,
							'ProductModelId':  mid,
							'PriceUnits': price_unit,
							'imgCaptcha': ver_code
						}
						r = requests.post(create_url, data=data, headers=headers1)
						key_obj = json.loads(r.text)
							
				print(key_obj['data'])
				key = key_obj['data']['redirectUrl'].split('/')[-1]
				#print(key)
				return key
				
			else:
				print('响应错误：', key_obj)
				return None
			
		except:
			#time.sleep(1)
			print('xxxxxxxxxxxxxxxxxxxxxx')
					
	else:
		print(r.status_code)
		return None
		
		
		
def get_price(pid, key, price_unit, f):                     #获取并写入价格
	
	inquiry_url = 'https://www.aihuishou.com/portal-api/inquiry/'
	product_url = 'https://www.aihuishou.com/product/'
	
	data_ids_all = get_ids_all(product_url+pid+'.html', headers)
	id_values = get_id_values(product_url+pid+'.html')
	
	r = requests.get(inquiry_url+key, headers=headers)
	if r.status_code == 200:
		price_obj = json.loads(r.text)
		print(price_obj['data'])
		print('------------------------*****************------------------------')
		price = price_obj['data']['amount']
		name = price_obj['data']['product']['productName']
		
		price_unit_lst = price_unit.split(';')
		for i in price_unit_lst:           #将没有value的id去除
			if i not in list(id_values.keys()):
				price_unit_lst.remove(i)
				
		price_unit_sorted = []
		for i in range(len(data_ids_all)):      #对id进行重新排序
			n = 0
			while n < len(price_unit_lst):
				if price_unit_lst[n] in data_ids_all[i]:
					price_unit_sorted.append(price_unit_lst[n])
					break
				n += 1
		
		
		values_lst = []
		
		for i in price_unit_sorted:
			values_lst.append(id_values[i])
		values = ','.join(values_lst)
		
		#f = open(r'E:\Spider\爱回收\Result\123.csv', 'a', encoding='utf-8')
		f.write('%s,%s,%s' %(price, name, values) + '\n')
		f.flush()
		
		#print('%s,%s,%s' %(price, name, values) + '\n')
		return None
		
	else:
		print(r.status_code)
		return None
		
		
				
def save_pic(url):                           #保存验证码图片
	path = 'E:\Spider\爱回收\Images\\'
	file_name = url.split('/')[-1] + '.jpg'
	file_path = path + file_name
	r = requests.get(url, headers=headers)
	with open(file_path, 'bw') as f:
		f.write(r.content)
		
		


def main(pid, price_unit):
	
	f = open(r'E:\Spider\爱回收\Result\20181017\锤子 坚果 Pro2S_price.csv', 'a', encoding='utf-8')
	key = get_key(pid, price_unit)
	#print(key)
	get_price(pid, key, price_unit, f)
	
	
	
if __name__ == '__main__':
	pid = '27501'
	price_units = open(r'E:\Spider\爱回收\Result\20181017\id_units\锤子 坚果 Pro2S_units.txt').readlines()
	for price_unit in price_units:
		price_unit = price_unit.replace('\n', '')
		main(pid, price_unit)
	print('---------------------共%s条数据，已抓取完毕！----------------------'%(str(len(price_units))))


