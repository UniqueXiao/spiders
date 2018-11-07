#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import re



def get_ids_all(url, headers):    #获取所有选项id
	r = requests.get(url, headers=headers)
	
	if r.status_code == 200:
		
		html = etree.HTML(r.text)
		data_ids_all = html.xpath('//div[contains(@class, "select-property")]/dl')
		data_ids = []    #所有选项的id列表
		
		for dl in data_ids_all:
			data_id = dl.xpath('./dd/ul/li/@data-id')
			if data_id == [] or data_id[0] == '':
				continue
			else:
				data_ids.append(data_id)
				
		return data_ids
		
	else:
		print(r.status_code)
		return None




def get_base_infos(url):            #获取所有靓机价的基本信息id组合
	r = requests.get(url, headers=headers)
	
	if r.status_code == 200:
		
		html = etree.HTML(r.text)
		base_infos_str = str(html.xpath('//div[@id="group-property"]/@data-sku-property-value-ids')[0])
		
		if base_infos_str == '[[]]':
			return None
		else:
			base_infos_lst = re.findall('\d+', base_infos_str)
			#n = len(html.xpath('//div[@class="select-property base-property"]/dl'))  #基本信息选项
			n = 2
			base_infos = [base_infos_lst[i:i+n] for i in range(0, len(base_infos_lst), n)]
		
		#print(len(base_infos))
		return base_infos
		
	else:
		print(r.status_code)
		return None 
		

	

	
def generate_id_options(data_ids, qx_id='2124'):     #生成所有估价的id选项组合(不包含基本信息), qx_id为全新机选项id
	id_options_all = []
	
	for i in range(len(data_ids)):   
		
		if i == 0:
			id_options = []
			
			for id in data_ids[i]:
				id_option = [id]
				n = 1
				while n < len(data_ids) - 1:
					if data_ids[n][0] == qx_id:
						id_option.append(data_ids[n][1])
					else:
						id_option.append(data_ids[n][0])
					n += 1
				id_options.append(id_option)
			
			id_options_all += id_options
			#print(len(id_options_all))
		
		elif i < len(data_ids) - 1:
			id_options = []
			
			if qx_id in data_ids[i]:
				data_id_tem = data_ids[i][:]
				data_id_tem.remove(data_ids[i][1])
			else:
				data_id_tem = data_ids[i][1:]
				
			for id in data_id_tem:
				id_option = [id]
				n, m = 1, 1
				
				while n - 1 < i:
					if data_ids[n-1][0] == qx_id:
						id_option.insert(n-1, data_ids[n-1][1])
					else:
						id_option.insert(n-1, data_ids[n-1][0])
					n += 1
					
				while m+i < len(data_ids) - 1:
					if data_ids[m+i][0] == qx_id:
						id_option.append(data_ids[m+i][1])
					else:
						id_option.append(data_ids[m+i][0])
					m += 1
				id_options.append(id_option)
				
			id_options_all += id_options
			#print(len(id_options_all))
			
		elif i == len(data_ids) - 1:
			id_options = []
			
			for id in data_ids[i]:
				id_option = [id]
				n = 1
				while n - 1 < i:
					if data_ids[n-1][0] == qx_id:
						id_option.insert(n-1, data_ids[n-1][1])
					else:
						id_option.insert(n-1, data_ids[n-1][0])
					n += 1
				id_options.append(id_option)
				
			id_options_all += id_options
			#print(len(id_options_all))
			
	
	return id_options_all

	


	
def generate_id_units(id_options, base_infos, qx_id='2124'):      #生成所有包含基本信息id选项组合
	
	id_units = []
	
	if base_infos == None:
		for id_option in id_options:
			id_unit = ';'.join(id_option)
			id_units.append(id_unit)	
		
		return id_units
		
	else:
		if id_options[0][0] == qx_id:              #如果首项为全新机，则用第二项与基本信息组合生成所有靓机的估价id组合
			
			for base_info in base_infos:                
				base_info_unit = base_info + id_options[1]
				id_units.append(';'.join(base_info_unit))
				
		else:
			for base_info in base_infos:                
				base_info_unit = base_info + id_options[0]
				id_units.append(';'.join(base_info_unit))
		
		for id_option in id_options:
			id_units.append(';'.join(base_infos[0] + id_option))
			
		return id_units
		
			



def main(url):
	
	r = requests.get(url, headers=headers)
	html = etree.HTML(r.text)
	info_num = len(html.xpath('//div[@class="select-property base-property"]/dl'))   #基本信息选项数量
	
	data_ids = get_ids_all(url, headers)[info_num:]
	base_infos = get_base_infos(url)
	id_options = generate_id_options(data_ids)
	#print(len(id_options))
	id_units = generate_id_units(id_options, base_infos)
	with open(r'E:\Spider\爱回收\Result\20181017\id_units\锤子 坚果 Pro2S_units.txt', 'a', encoding='utf-8') as f:
		print('id组合数量：',len(id_units))
		for i in id_units:
			f.write(i + '\n')
			f.flush()
			
			
'''			
phone_qx_id = '2124'   #手机全新机选项id
pad_qx_id = '1983'     #平板全新机选项id
laptop_qx_id = '4475'  #笔记本全新机选项id

df_qx_id = '5676'  	   #单反相机全新机选项id
sm_qx_id = '2398'  	   #数码相机全新机选项id
jt_qx_id = '5677'  	   #镜头全新机选项id
wd_qx_id = '2375'  	   #微单全新机选项id
sx_qx_id = '3809'  	   #摄像机全新机选项id
sg_qx_id = '4799'  	   #闪光灯全新机选项id
'''	
			
if __name__ == '__main__':
	
	url = 'https://www.aihuishou.com/product/27501.html'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3381.1 Safari/537.36'}
	
	main(url)