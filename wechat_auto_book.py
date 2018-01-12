#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
import time
import sys
import argparse
reload(sys)
sys.setdefaultencoding('utf8')


cookies = {
	"public_account": "cwbnXAa4HxSuKBOzLRiuHwulbVLjaijiHxmlLR.vLBWyMRClJAb1XULmWVPHXAa4H03zZEulJAbjZUDnZAa4HxC2LhGuKx.uMBOuOBCxMQ3hZ0ylJAbrZ0HnZESlMgavMBWwKBKuKBeyKAaqH1HjWUvMWUzjHxml3Jgj3WsF3nYFHwulW07raEDscSjiHxmlKR.uLhWyHwulW07raEDscS3fZUSlMgdkr5FjlJNjsGJjhXdjqZFjhJpkjmdjhHZitXNmepJjqW.ldO",
	"JSESSIONID": ""
}

def get_target_id():
	url = "http://www.nswtt.org.cn/pubService/dataList.do"
	form = {
		"page": 1,
		"rows": 2,
		"objectId": 102599
	}

	ret = requests.post(url, data=form, cookies=cookies).json()
	'''                                                                                                                                                                                                                             [m:Auto]
{
    "count": 16, 
    "page": 2, 
    "pubServiceId": "100384,100383,100382,100381,100380,100379,100378,100377,100376,100375", 
    "rows": [
        {
            "dataContent": null, 
            "givePrice": "0.0", 
            "id": 100384, 
            "marketPrice": "0.0", 
            "picUrl": "http://cdnimg.ydmap.com.cn/pubservice/197755/", 
            "salesPrice": "0.0", 
            "serviceName": "单人券01-03"
        }, 

	'''
	#print(ret["pubServiceId"])
	target_id = ret["pubServiceId"].split(",")[1]
	return target_id

def print_ret(ret):
	for key, value in ret.items():
		print("{}: {}".format(key, value))

def book_target_and_get_payment_id(target_id):
	i = 0
	url = "http://www.nswtt.org.cn/v2/pubService/save.do"
	form = {
		"pubServiceId": target_id,
		"num": 1
	}
	while(True):
		ret = requests.post(url, data=form, cookies=cookies).json()
		print_ret(ret)
		if ret['code'] != 200 and i < 6:
			i += 1
			time.sleep(5)
			continue
		break
	'''
		{
		    "code": 200, 
		    "data": 1167116, 
		    "msg": "成功"
		}
	'''
	return ret["data"]

def result_inform(content):
	data = {
		"send_type": "wechat",
		"to": "xn080520",
		"content": content
	}
	requests.post("https://ops-amc.niudingfeng.com/send", json=data).json()

def pay_target(payment_id):
	url = "http://www.nswtt.org.cn/v2/pay/pubAccountPay.do"
	form = {
		"dealId": payment_id,
		"payMode": 5, 
		"pubServiceAccountId": None
	}
	ret = requests.post(url, data=form, cookies=cookies).json()
	'''
	{
	    "code": 200, 
	    "data": 1167116, 
	    "msg": "成功"
	}

	'''
	result_inform(ret["msg"])
	return ret

def input_jsessionid():
	parser = argparse.ArgumentParser()
	parser.add_argument('JSESSIONID', type=str, 
                    help='JSESSIONID of wechat when you visit www.nswtt.org.cn. I use mitmproxy to get JSESSIONID')
	args = parser.parse_args()
	return args.JSESSIONID

def main():
	jsessionid = input_jsessionid()
	global cookies
	cookies['JSESSIONID'] = jsessionid

	target_id = get_target_id()
	print("target_id is {}".format(target_id))
	pay_id = book_target_and_get_payment_id(target_id)
	print("pay_id is {}".format(pay_id))
	ret = pay_target(pay_id)
	print_ret(ret)

if __name__ == '__main__':
	main()

	












