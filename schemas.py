from typing import Union
from fastapi import Query
from pydantic import BaseModel

class Address(BaseModel):
    first_name:str = Query(min_length=1,max_length=25)
    last_name: Union[str, None] = None
    age:int = Query(ge=0000000000,le=9999999999)
    mobile_no:str = Query(max_length=10,min_length=10)
    city:str
    state:str
    country:str
    latitude:float  = Query(ge=-90, le=90)
    longitude:float = Query(ge=-180, le=180)

class Coords(BaseModel):
    latitude:float  = Query(ge=-90, le=90)
    longitude:float = Query(ge=-180, le=180)
    distance_in_km:float = Query(ge=0, le=99999)
