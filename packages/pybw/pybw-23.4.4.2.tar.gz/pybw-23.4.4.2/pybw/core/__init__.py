# -*- coding: utf-8 -*-
"""
author: Bowei Pu at 2023.03.01
version: 2023.03.14
function: Some useful tools
"""

from pybw.tricks.lazy_import import *


__author__ = 'Bowei Pu'
__version__ = '2023.03.11'
__maintainer__ = 'Bowei Pu'
__email__ = 'pubowei@foxmail.com'
__status__ = 'Beta'
__date__ = '2023-03-11'


def time_parser(sec):
    s = int(sec)
    m, sec = s // 60, s % 60
    h, mins = m // 60, m % 60
    day, hour = h // 24, h % 24
    return {'day': day, 'hour': hour, 'min': mins, 'sec': sec, 's': s}


def getsizeof(obj):
    return sys.getsizeof(pickle.dumps(obj))


class EasyPickle():
    '''
    Easy usage for pickle
    '''
    def __init__(self):
        self._function = 'Easy usage for pickle'
    
    @classmethod
    def dump(cls, obj, file_obj):
        pickle.dump(obj, file_obj)
    
    @classmethod
    def load(cls, file_obj):
        return pickle.load(file_obj)
    
    @classmethod
    def save(cls, obj, file):
        if not os.path.exists(Path(file).parent):
            os.makedirs(Path(file).parent)
        with open(file, 'wb') as f:
            pickle.dump(obj, f)
    
    @classmethod
    def read(cls, file):
        with open(file, 'rb') as f:
            return pickle.load(f)


class easypickle(EasyPickle):
    def __init__():
        EasyPickle.__init__(self)


class PickleDump(EasyPickle):
    '''
    Compatible to old version programs
    '''
    def __init__():
        EasyPickle.__init__(self)


class DictDoc():
    '''
    Pack dict to class for easy use
    '''
    def __init__(self, dic: dict={}):
        self.dic = dic
        self._generate_attributes()
    
    def __repr__(self):
        return '<DictDoc>'
    
    def __str__(self):
        return self.__repr__()
        
    def dict(self):
        return self.dic
    
    def as_dict(self):
        return self.dic
    
    def keys(self):
        return self.dic.keys()
    
    def values(self):
        return self.dic.values()
    
    def _generate_attributes(self):
        for k, v in self.dic.items():
            setattr(self, k, v)
    
    def setattr(self, name, value):
        self.dic[name] = value
        setattr(self, name, value)
    
    def add(self, name, value):
        self.setattr(name, value)
    
    