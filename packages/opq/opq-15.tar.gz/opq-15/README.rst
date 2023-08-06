README
######

**NAME**

|
| ``opq`` - object programming quest
|

**SYNOPSIS**


The ``opq`` package provides an Object class, that allows for save/load to/from
json files on disk. Objects can be searched with database functions and have a 
type in filename for reconstruction. Methods are factored out into functions to
have a clean namespace to read JSON data into.

This is the quest for object programming (OP), the OOP without the oriented.

|

**INSTALL**

|
| ``python3 -m pip install opq --upgrade --force-reinstall``
|

**PROGRAMMING**

basic usage is this::

 >>> import opq
 >>> o = opq.Object()
 >>> o.key = "value"
 >>> o.key
 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

read/write from/to disk::

 >>> from opq import Object, read, write
 >>> o = Object()
 >>> o.key = "value"
 >>> p = write(o)
 >>> obj = Object()
 >>> read(obj, p)
 >>> obj.key
 'value'

great for giving objects peristence by having their state stored in files::

 >>> from opq import Object, write
 >>> o = Object()
 >>> write(o)  # doctest: +ELLIPSIS
 'opq.objects.Object/...'

|

**AUTHOR**

|
| B.H.J. Thate <operbot100@gmail.com>
|

**COPYRIGHT**

|
| ``opq`` is placed in the Public Domain.
|
