hitlib2
=======

Tiny Python library servering as a set of APIs for HIT Online Library

##Usage:

```python
>>> from hitlib2 import Query
>>> f = Query("Python", "sm") #sm : shumu
>>> f.show()
>>> f.show("title")
>>> f.origin()

```
##TODO:

* you can just type in the console or bash window as below:

```bash
~$ python hitlib2.py Python
~$ chmod +x hitlib2.py
~$ ./hitlib2.py Python
~$ ./hitlib2 Python -c QK  #QK means QIKAN
```

* build a package, publish to the PyPI

