from fastapi import FastAPI, Body, Depends, HTTPException as excep,Path
import schemas
import models
import os
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session 
import logging
import geopy.distance


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Helper method used to get distance of given co-ords.
def get_distance_in_km(coords1:float,coords2:float):
    """ input: coords1->float
               coords2->float
               
        returns: float
            distance in km.
    """
    return geopy.distance.geodesic(coords1, coords2).km

Base.metadata.create_all(engine)

# Load session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()

# List of dict dummy data
fakeDatabase = [
    {'first_name':'Arun','last_name':'Menon','age':24,'mobile_no':1234567890,'city':'Bangalore','state':'Karnataka','country':'India','latitude':41.40338,'longitude':2.17403},
    {'first_name':'Prabhu','last_name':'Deva','age':23,'mobile_no':1234567899,'city':'Bangalore','state':'Karnataka','country':'India','latitude':41.54961,'longitude':1.87754},
    {'first_name':'Harry','last_name':'Prakash','age':24,'mobile_no':1234567898,'city':'Bangalore','state':'Karnataka','country':'India','latitude':41.06374,'longitude':1.51681},
]

version = "/v1"

# List out all address
@app.get(os.path.join(version,"address/list"))
def getItems(session: Session = Depends(get_session)):
    log.info("Get all records from the address book!")
    addresses = session.query(models.Address).all()
    if addresses:
        return addresses
    else:
        raise excep(status_code=404, detail="Nothing to return address book was empty!")

# Get address by id
@app.get(os.path.join(version,"address/fetch/{id}"))
def getItem(id:int, session: Session = Depends(get_session)):
    log.info("Get address by given Id!")
    address = session.query(models.Address).get(id)
    if address:
        return address
    else:
        raise excep(status_code=404,detail=f"Given Id {id} was not found in the address book master!")

# Get address by km from the given coords
@app.post(os.path.join(version,"address/distance"))
def getAddressByCoords(data:schemas.Coords,session: Session = Depends(get_session)):
    log.info("Retrieve Address list by coords and distance!")
    addresses = session.query(models.Address).all()
    list_of_address = []
    for address in addresses:
        km = get_distance_in_km((address.latitude,address.longitude),(data.latitude,data.longitude))
        if km <= data.distance_in_km:
            list_of_address.append(address)
    if list_of_address:
        return list_of_address
    else:
        raise excep(status_code=404,detail="No addresses found by given coords and distance!")

# Return Dummy data from dict
@app.post(os.path.join(version,"address/dummy"))
def dummyAddresses():
    return fakeDatabase

# Load dummy data into database
@app.post(os.path.join(version,"address/create"))
def addItem(data:schemas.Address, session: Session = Depends(get_session)):
    address = models.Address(first_name = data.first_name,last_name=data.last_name,\
        age=data.age,mobile_no=data.mobile_no,city=data.city,state=data.state,country=data.country,\
            latitude=data.latitude,longitude=data.longitude)
    
    session.add(address)
    session.commit()
    session.refresh(address)
    return address

# Update address by id
@app.put(os.path.join(version,"address/update/{id}"))
def updateItem(id:int, address:schemas.Address, session: Session = Depends(get_session)):
    log.info(f"Update Id {id} by given details!")
    itemObject = session.query(models.Address).get(id)
    if itemObject:
        itemObject.first_name = address.first_name
        itemObject.last_name = address.last_name
        itemObject.age = address.age
        itemObject.mobile_no = address.mobile_no
        itemObject.city = address.city
        itemObject.state = address.state
        itemObject.country = address.country
        itemObject.latitude = address.latitude
        itemObject.longitude = address.longitude
        session.commit()
        return itemObject
    else:
        raise excep(status_code=404,detail=f"Given Id {id} was not found in the Address book master!")

# Delete address by id
@app.delete(os.path.join(version,"address/delete/{id}"))
def deleteItem(id:int, session: Session = Depends(get_session)):
    log.info(f"Delete address by given ID {id}!")
    itemObject = session.query(models.Address).get(id)
    if itemObject:
        session.delete(itemObject)
        session.commit()
        session.close()
        return {'detail':'Address was deleted successfully!'}
    else:
        raise excep(status_code=404,detail=f"Given ID {id} was not found in the address book master!")