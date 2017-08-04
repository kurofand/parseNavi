
# -*- coding: utf-8 -*

import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import time
import os.path

def getHTML(url):
	try:
		html=requests.get(url)
	except requests.eceptions.ConnectionError:
		time.sleep(300)
		html=requests.get(url)
	data=html.text
	body=BeautifulSoup(data, 'lxml')
	return(body)

shopTypes=['0201', '0202']
#тут менять параметр после категории для перехода по магазинам/конбини
#выдирать значения можно непосредственно из селектов
#0201 - конбини
startTime=datetime.now();
recordCount=0
for shopType in shopTypes:
	body=getHTML('https://www.navitime.co.jp/category/%s'%shopType)
	shops=body.find('select', {'id':'detail_category_id_select'}).findChildren('option')
	for shop in shops:
		if((shop['value']!="") and (shop['value']!="%s001003"%shopType)):
			body=getHTML('https://www.navitime.co.jp/category/%s'%shop['value'])
			selectPref=body.find('select', {'id':'prefecture_select'})
			prefList=selectPref.findChildren('option')
			for prefecture in prefList:
				#сейчас только Токио, поэтому только 13
				if(prefecture['value']=="13"):
					fPath='txt_files/%s.txt'%prefecture.text
					
					if not(os.path.exists(fPath)):
						file=open(fPath, 'w')
					else:
						file=open(fPath, 'a')
					html=requests.get('https://www.navitime.co.jp/async/category/addressList?addressCode=%s'%prefecture['value'])
					js=json.loads(html.text)
					for code in js:
						page=1
						while True:
							#тут тоже не забудь поменять параметр после категории
							#time.sleep(5)
							body=getHTML('https://www.navitime.co.jp/category/%s/%s?page=%s'%(shop['value'], code['code'], page))
							linkDiv=body.find('div', {'id':'spot_list'})
							linkDl=linkDiv.findChildren('dl', {'class':'list_item_frame'})
							if(linkDl):
								page=page+1
								for dl in linkDl:
									link=dl.find('a')
									name=link.text
									addr=dl.find('dd').contents[0]
									file.write('%s\n%s\n'%(name.encode('utf-8'), addr.encode('utf-8')))
									recordCount=recordCount+1
							else:
								break
						print('%s has done'%code['name'])
					file.close()
print('%s has done'%prefecture.text)
print('All done, %s records writed'%recordCount)
endTime=datetime.now()
print('It taked %s'%str(endTime-startTime))
