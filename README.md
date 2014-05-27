hitlib2
=======

Tiny Python library servering as a set of APIs for HIT Online Library

##Usage:

####Simple Query
```python
>>> from hitlib2 import Query
>>> f = Query("Python", "sm") # sm : shumu
>>> f.show() # same as f.show('title')
Exploring python 
真实世界的Python仪器监控
Python入门经典
Head First Python
......
```
####Book and shelf detail
```python
>>> f.origin().show_book() # same as f.origin.show_book()(0)
Exploring python 
Budd Timothy A. Timothy A. Budd.
Mc Graw Hill Higher Education,
c2010.
278 p. :
TP312PYB927
210000000724250
>>> f.origin().show_shelf()
1000172846		一区外文样本(501-1)		外文书		在馆	
>>> 


```

Or you can just type in the console or bash window as below:

```bash
$ python hitlib2.py
usage: hitlib2.py [-h] [-t TYPE] [-a ALL] [-p POS] [QUERY [QUERY ...]]

Tiny Python library servering as a set of APIs for HIT Online Library

positional arguments:
  QUERY                 query the book info

optional arguments:
  -h, --help            show this help message and exit
  -t TYPE, --type TYPE  book type of query: sm (shumu), qk (qikan), lw
                        (lunwen)
  -a ALL, --all ALL     display the full info of the result
  -p POS, --pos POS     select book info in specified position (default: 1)


$ python hitlib2.py Python
Exploring python 
真实世界的Python仪器监控
Python入门经典
Head First Python
Python计算与编程实践
Python科学计算
Python编程实践
Head first Python 
Programming Python 
Python Web开发学习实录

$ python hitlib2.py 热处理 -t lw
纯钛和BT20钛合金筒形件旋压织构及在热处理中的演化
3J33(AB)马氏体时效钢强韧化热处理工艺及力学性能
20CrMoH齿轮用钢热处理工艺研究
热处理对锻造态 -TiAl基合金组织及力学性能影响
热处理工艺对SWRH72A钢丝绳疲劳寿命影响的研究
20CrMoH齿轮用钢热处理工艺研究
磁记忆用于材料热处理质量评估的方法研究
热处理工艺对7150 铝合金组织和性能影响的研究
0Cr11Ni2MoVNb合金的热处理工艺优化及组织和性能
NiCrW铸造高温合金热处理及组织结构与力学性能
```
ToDO
* build a package, publish to the PyPI

