# -*- coding: utf-8 -*-  
import requests
import random
import json
import pymysql
import time
import hashlib

url_1 = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city='
url_2 = '&needAddtionalResult=false&kd='
headers = {'Host':'www.lagou.com','User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36','Cookie':'user_trace_token=20170208130109-9aaa0404-edbb-11e6-8f61-5254005c3644; LGUID=20170208130109-9aaa0719-edbb-11e6-8f61-5254005c3644; JSESSIONID=F3F361CEED0ACD3F17112753569325C6; _putrc=00C6A03A01332BEB; login=true; unick=%E6%9D%8E%E6%98%8E%E8%88%AA; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=152; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_iOS%3Fpx%3Ddefault%26city%3D%25E6%25B7%25B1%25E5%259C%25B3; _gat=1; TG-TRACK-CODE=index_navigation; SEARCH_ID=4d90963f818446059da0cbf0bdf0b2ba; index_location_city=%E5%B9%BF%E5%B7%9E; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1488005231,1488419706,1488419773,1488504600; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1488510382; _ga=GA1.2.372407027.1486530069; LGSID=20170303104240-11e969ec-ffbb-11e6-a9fb-525400f775ce; LGRID=20170303110621-6110009b-ffbe-11e6-918d-5254005c3644','Referer':'https://www.lagou.com/jobs/list_php?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput='}

jobs = ['iOS','Android','php','java','python','C++','web']
citys = ['北京','上海','深圳','杭州','广州','成都','武汉']
citys_utf8 = {'北京':'beijing','上海':'shanghai','深圳':'shenzhen','杭州':'hangzhou','广州':'guangzhou','成都':'chengdu','武汉':'wuhan'}

def getCityInfo(city):
	result_job = {}
	for job in jobs:
		url = url_1 + city + url_2 + job
		r = requests.get(url,headers=headers)
		binary = r.content.decode('utf-8')
		data = json.loads(binary)
		print(data)
		count = str(data['content']['positionResult']['totalCount'])
		createTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		city_utf8 = 'utf8'
		city_utf8 = citys_utf8[city]
		src = city_utf8 + job + createTime
		# print(src+'======')
		result_sha1_value=get_md5_value(src.encode('utf8'))
		mysqlBlock(city_utf8,job,count,createTime,result_sha1_value)

def mysqlBlock(lg_location,lg_job,lg_count,lg_time,md5):
	sqli="insert IGNORE into lagou values(NULL,%s,%s,%s,%s,%s)"
	# sqli="insert into lagou values(NULL,%s,%s,%s,%s,%s)"
	cursor.execute(sqli,(lg_location,lg_job,lg_count,lg_time,md5))

def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

def get_sha1_value(src):
    mySha1 = hashlib.sha1()
    mySha1.update(src)
    mySha1_Digest = mySha1.hexdigest()
    return mySha1_Digest

host="localhost"
user='root'
passwd='pwd'
db='dbname'
conn=pymysql.connect(host,user,passwd,db)
cursor=conn.cursor()

for city in citys:
	stime = random.randint(6, 10) 
	time.sleep(stime)
	cityResult = getCityInfo(city)

cursor.close()
conn.commit()
conn.close()

	
