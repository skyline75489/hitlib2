#! /usr/bin/env python
# -*- coding: utf-8 -*- 
import argparse
import re
import sys

import requests
from BeautifulSoup import BeautifulSoup

BASE_URL = "http://202.118.250.131/lib/opacAction.do?method=DoAjax&dispatch=smcx&type=smcx&method1=1&retrieveLib=1"
BOOK_DETAIL_URL = "http://202.118.250.131/lib/opacAction.do?method=DoAjax&dispatch=searchBiblInfo&type=searchBiblInfo&book_type=589&currpage=1&id_bibl="

#书目
SM_TYPE="589"
#期刊
QK_TYPE="590"
#论文
LW_TYPE="666"


def _make_sm_dict(info):
    return Book({'title':info[0], 'author':info[1], 'publisher':info[2], 
                 'year':info[3], 'pages':info[4], 'sn':info[5], 'id':info[7]})

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

class Book(dict):

    def _request_for_detail(self):
    	try:
    		response = requests.get(BOOK_DETAIL_URL + str(self['id']))
    	except requests.exceptions.RequestException as e:
            print(e.message)
            
        self._detail_raw = response.content
        return BeautifulSoup(self._detail_raw)

    def _parse_detail(self, f):
        self['shelf'] = []
        a = f.findAll('td')
        list_len = len(a)
        for i in range(47, list_len-4, 4):
            shelf_info = {}
            shelf_info['num'] = a[i].text
            shelf_info['pos'] = a[i+1].text
            shelf_info['type'] = a[i+2].text
            shelf_info['status'] = a[i+3].text
            shelf_info['return'] = a[i+4].text
            if not shelf_info['num'] or not shelf_info['pos']:
                continue
            for k in shelf_info.keys():
                if shelf_info[k].find('nbsp') > 0:
                    return
            self['shelf'].append(shelf_info)

    def _get_result(self):
        if self.has_key('shelf'):
            return self['shelf']

        self._parse_detail(self._request_for_detail())
        return self['shelf']

    def show_book(self):
    	print(unicode('{0[title]}\n'
    		          '{0[author]}\n'
    		          '{0[publisher]}\n'
    		          '{0[year]}\n'
    		          '{0[pages]}\n'
    		          '{0[sn]}\n'
    		          '{0[id]}').format(self))

    def show_shelf(self):
        for i in self._get_result():
            print(unicode('{0[num]}\t\t{0[pos]}\t\t{0[type]}\t\t{0[status]}\t{0[return]}').format(i))
            

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

        self.result = self._parse_html(self._requests())
        return self.result
        
    def _requests(self):
        try:
            response = requests.get(BASE_URL + "&title=" + self.keyword + "&pabookType=" + 
                       self.typeMap[self.q_type] + "&smcx_p=" + str(self.page))
        except requests.exceptions.RequestException as e:
            print(e.message)
            
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

def get_parser():
    parser = argparse.ArgumentParser(description='Tiny Python library servering as a set of APIs for HIT Online Library')
    parser.add_argument('query', metavar='QUERY', type=str, nargs='*',
                        help='query the book info')    
    parser.add_argument('-t', '--type', help='book type of query: sm (shumu), qk (qikan), lw (lunwen)', default='sm', type=str)    
    parser.add_argument('-a','--all', help='display the full info of the result')
    parser.add_argument('-p','--pos', help='select book info in specified position (default: 1)')

    return parser

def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if not args["query"]:
        parser.print_help()
        return

    query(args)
    return

def query(args):
    f = Query(' '.join(args['query']), args['type'])
    if args['pos']:
        print(f.origin(int(args['pos'])))
        return

    f.show()

if __name__ == '__main__':
    command_line_runner()
