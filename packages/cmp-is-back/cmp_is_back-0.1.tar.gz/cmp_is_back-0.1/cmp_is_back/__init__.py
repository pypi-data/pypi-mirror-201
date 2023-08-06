def cmp(a, b) :
    """cmp(x, y) -> integer

Return negative if x<y, zero if x==y, positive if x>y."""
    
    return (a>b) - (a<b)

class CmpIsBack :
    """Make __cmp__ rework.
NOTE: In Python 1 and 2, it does nothing.

>>> class MyInt(CmpIsBack) :
...     def __init__(self, a=0) :
...         self.a = int(a)
...     def __cmp__(self, value) :
...         return (self.a>self.b) - (self.a<self.b)
...
>>> MyInt(10) > MyInt(9)
True
>>> MyInt(9) < MyInt(10)
True
"""
    
    try :
        long
    except NameError :
        def __eq__(self, value) :
            """x.__eq__(y) <==> x==y"""
            
            try :
                return self.__cmp__(value) == 0
            except AttributeError :
                return id(self) == id(value)
        
        def __ne__(self, value) :
            """x.__ne__(y) <==> x!=y"""
            
            try :
                return self.__cmp__(value) != 0
            except AttributeError :
                return id(self) != id(value)
        
        def __gt__(self, value) :
            """x.__gt__(y) <==> x>y"""
            
            try :
                return self.__cmp__(value) > 0
            except AttributeError :
                return id(self) > id(value)
        
        def __ge__(self, value) :
            """x.__ge__(y) <==> x>=y"""
            
            try :
                return self.__cmp__(value) >= 0
            except AttributeError :
                return id(self) >= id(value)
        
        def __lt__(self, value) :
            """x.__lt__(y) <==> x<y"""
            
            try :
                return self.__cmp__(value) < 0
            except AttributeError :
                return id(self) < id(value)
        
        def __le__(self, value) :
            """x.__le__(y) <==> x<=y"""
            
            try :
                return self.__cmp__(value) <= 0
            except AttributeError :
                return id(self) <= id(value)
        
        def __hash__(self) :
            return object.__hash__(self)
