#! /usr/bin/env python
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


class Query(object):

    def __init__(self, keyword, q_type="sm", page=1):
        self.keyword = keyword
        self.page = page
        #cache the result
        self.result = None
        self.raw = None
        self.q_type = q_type.lower()
        
        if q_type not in ("sm", "qk", "lw"):
            raise TypeError("Wrong type")

        self.typeFunctionMap = {
            "sm": _make_sm_dict,
            "qk": _make_qk_dict,
            "lw": _make_lw_dict
        }

        self.typeMap = {
            "sm": SM_TYPE,
            "qk": QK_TYPE,
            "lw": LW_TYPE
        }

    def show(self, keyword = "title"):
        for i in self._get_result():
            if isinstance(i, dict):
                print(i[keyword])

    def origin(self, num=0):
        return self._get_result()[num]

    def _get_result(self):
        # already cached
        if self.result:
            return self.result

        result = self._parse_html(self._requests())
        self.result = result
        return result
        
    def _requests(self):
        try:
            response = requests.get(BASE_URL + "&title=" + self.keyword + "&pabookType=" + 
                       self.typeMap[self.q_type] + "&smcx_p=" + str(self.page))
        except requests.exceptions.RequestException as e:
            print e.message
            
        self.raw = response.content
        return BeautifulSoup(self.raw)

    def _parse_html(self, f):
        return [self.typeFunctionMap[self.q_type](self._digest_info(tr)) for tr in 
                f.findAll(onmouseover=True)]

    def _digest_info(self, tr):
        info = []
        id_reg = re.compile(r'showDetail\(\'(\d*)\'\,')
        id_text = tr.find(onclick=True)['onclick']
        for td in tr.findAll("td"):
            # remove strange characters
            text = td.text.replace("/", "")
            text = text.replace("=", "")
            text = text.replace("\x1e", " ")
            info.append(text)
            
        # the id for more detail
        info.append(int(id_reg.findall(id_text)[0]))
        return info

if __name__ == '__main__':
    f = Query("python")
    f.show()
    f.show("title")
    f.origin()
    
    
