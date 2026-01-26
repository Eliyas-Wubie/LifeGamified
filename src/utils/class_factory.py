from typing import Any
    
class ClassFactory:
    _instance = None
    
    def __new__(cls, *args:Any, **kwargs:Any):
        if not cls._instance:
            cls._instance=super().__new__(cls)
        return cls._instance
    
    def create_class(self, class_name:str, base_class:Any, attrs:dict[str, Any]| None):
        if attrs is None:
            attrs={}
        
        def __init__(self:Any, *args:Any, **kwargs:Any):
            base_class.__init__(self, *args, **kwargs)
        
        attrs["__init__"] = __init__
        try:
            return type(class_name, (base_class,), attrs)
        
        except TypeError as e:
            raise TypeError(f"failed to create class {class_name} : {e}")
