# -*- coding: utf-8 -*- 

import re
import requests
from BeautifulSoup import BeautifulSoup

BASE_URL = "http://202.118.250.131/lib/opacAction.do?method=DoAjax&dispatch=smcx&type=smcx&method1=1&retrieveLib=1"

#书目
SM_TYPE="589"
#期刊
QK_TYPE="590"
#论文
LW_TYPE="666"

def _request(title,query_type,page):
	response = None
	try:
		response = requests.get(BASE_URL + "&title=" + title + "&pabookType=" + query_type + "&smcx_p=" + str(page));
	except Exception as e:
		pass
	if response :
		return BeautifulSoup(response.content)
	else:
		raise TypeError("No response from server")

def _digest_info(tr):
	info = []
	id_reg = re.compile(r'showDetail\(\'(\d*)\'\,')
	id_text = tr.find(onclick=True)['onclick']
	for td in tr.findAll("td"):
		text = td.text.replace("/","")
		text = text.replace("=","")
		text = text.replace("\x1e"," ")
		info.append(text)
		
	info.append(int(id_reg.findall(id_text)[0]))
	return info

def _make_sm_dict(info):
	info_dict = {}
	info_dict['title'] = info[0]
	info_dict['author'] = info[1]
	info_dict['publisher'] = info[2]
	info_dict['year'] = info[3]
	info_dict['pages'] = info[4]
	info_dict['sn'] = info[5]
	info_dict['id'] = info[7]
	return info_dict

def _make_qk_dict(info):
	info_dict = {}
	info_dict['title'] = info[0]
	info_dict['enterprise'] = info[1]
	info_dict['publisher'] = info[2]
	info_dict['sn'] = info[5]
	info_dict['id'] = info[7]
	return info_dict

def _make_lw_dict(info):
	info_dict = {}
	info_dict['title'] = info[0]
	info_dict['author'] = info[1]
	info_dict['year'] = info[3]
	info_dict['sn'] = info[5]
	info_dict['id'] = info[7]
	return info_dict

def _resolve_html(html,query_type):
	trs = html.findAll(onmouseover=True)
	result_list = []
	for tr in trs:
		info = _digest_info(tr)
		row_dict = {}
		if query_type == SM_TYPE:
			row_dict = _make_sm_dict(info)
		if query_type == QK_TYPE:
			row_dict = _make_qk_dict(info)
		if query_type == LW_TYPE:
			row_dict = _make_lw_dict(info)

		result_list.append(row_dict)
	return result_list

def query(title, q_type="sm", page=1):
	"""
	query() can query book, magzine and paper
	"""
	query_type = SM_TYPE
	if q_type == "qk":
		query_type == QK_TYPE
	elif q_type == "lw":
		query_type == LW_TYPE
	
	html = _request(title,query_type,page)
	result = []
	result = _resolve_html(html,query_type)
	return result

def prettyprint(result_list,keyword="title"):
	"""
	prettyprint can print the value of given key
	of every result in the result_list
	"""
	for a in result_list:
		if isinstance(a,dict):
			print(a[keyword])
		else:
			raise TypeError("Non-dict type found in list")
