from typing import Any, TYPE_CHECKING
from src.models.domain.accomplishment import Accomplishment
if TYPE_CHECKING:
    from src.models.db.models import AccomplishmentORM

class AccomplishmentCache:
    _instance: "AccomplishmentCache | None" = None
    
    def __new__(cls, *args: Any, **kwargs:Any):
        if cls._instance is None:
            cls._instance=super().__new__(cls)
        return cls._instance
    def __init__(self) -> None:
        self._domain_cache: dict[int,"Accomplishment"]= {}
        self._orm_cache: dict[int,"AccomplishmentORM"]= {}

    @property
    def domain_cache(self):
        return self._domain_cache
    
    @domain_cache.setter
    def domain_cache(self, new_domain_cache:dict[int,"Accomplishment"]):
        self._domain_cache=new_domain_cache

    @property
    def orm_cache(self):
        return self._orm_cache
    
    @orm_cache.setter
    def orm_cache(self, new_orm_cache:dict[int,"AccomplishmentORM"]):
        self._orm_cache=new_orm_cache
    
    def query_domain_cache(self, domain:Any):
        key=id(domain)
        item=self._domain_cache.get(key)
        if not item:
            orm=self._orm_cache.get(key)
            key_orm=id(orm)
            item=self._domain_cache.get(key_orm)
        return item
    
    def query_orm_cache(self, orm:Any):
        key=id(orm)
        item=self._orm_cache.get(key)
        if not item:
            domain=self._domain_cache.get(key)
            key_domain=id(domain)
            item=self._orm_cache.get(key_domain)
        return item

    def query_inverse_cache(self, either:Any):
        if isinstance(either, Accomplishment):
            key=id(either)
            item=self._orm_cache.get(key)
            return item
        else:
            key=id(either)
            item=self._domain_cache.get(key)
            return item

    def add_to_cache(self, domain:Any = None, orm:Any = None):
        if domain is not None and orm is not None:
            key_domain=id(domain)
            key_orm=id(orm)
            
            # remove previous unrelated cache if any
            if key_domain in self._domain_cache:
                del self._domain_cache[key_domain]
            if key_orm in self._orm_cache:
                del self._orm_cache[key_orm]

            # creates if non existent and overwrites if exists
            self._domain_cache[key_orm]=domain
            self._orm_cache[key_domain]=orm
            
        elif domain is not None:
            key=id(domain)
            if key not in self._domain_cache and key not in self._orm_cache:
                self._domain_cache[key]=domain
        elif orm is not None:
            key=id(orm)
            if key not in self._domain_cache and key not in self._orm_cache:
                self._orm_cache[key]=orm
         
    def remove_domain_from_cache(self, domain:Any, remove_pair:bool=False):
        key=id(domain)
        if remove_pair:
            orm=self._orm_cache.get(key)
            key_orm=id(orm)
            del self._domain_cache[key_orm]
            del self._domain_cache[key]
            del self._orm_cache[key]
        elif key in self._orm_cache:
            orm=self._orm_cache.get(key)
            key_orm=id(orm)
            if orm is not None:
                self._orm_cache[key_orm]=orm
            del self._orm_cache[key]
               
    def remove_orm_from_cache(self, orm:Any, remove_pair:bool=False):
        key=id(orm)
        if remove_pair:
            domain=self._domain_cache.get(key)
            key_domain=id(domain)
            del self._orm_cache[key_domain]
            del self._orm_cache[key]
            del self._domain_cache[key]
        if key in self._domain_cache:
            domain=self._domain_cache.get(key)
            key_domain=id(domain)
            if domain is not None:
                self._domain_cache[key_domain]=domain
            del self._domain_cache[key]
    
    