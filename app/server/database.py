from pymongo import ASCENDING, DESCENDING
import motor.motor_asyncio
#from pymongo import MongoClient
#client = MongoClient()
from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.evedemo

people_collection = database.get_collection('people')


# helpers

def person_helper(person) -> dict:
    return {
        "id": str(person["_id"]),
        "email": person["email"],
        "name": person["name"]
    }


'''
# Normal way
def personEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "firstname": item["firstname"],
        "lastname": item["lastname"]
    }


def peopleEntity(entity) -> list:
    return [personEntity(item) for item in entity]


# Best way
def serializeDict(a) -> dict:
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}


def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]

'''

# crud operations


# Retrieve all people present in the database
async def retrieve_people(skip, limit, order_by):
    people = []
    # offset limit order_by filter
    # .sort([('time', 1)]).limit(3)  .skip(20).limit(10) .sort([("field1", pymongo.ASCENDING), ("field2", pymongo.DESCENDING)])
    #fake_items_db[skip : skip + limit]
    #total = people_collection.count_documents({})
    total = await people_collection.count_documents({})
    async for person in people_collection.find().skip(skip).limit(limit).sort([order_by]):
        people.append(person_helper(person))
    return [people, total]


# Add a new person into to the database
async def add_person(person_data: dict) -> dict:
    person = await people_collection.insert_one(person_data)
    new_person = await people_collection.find_one({"_id": person.inserted_id})
    return person_helper(new_person)


# Retrieve a person with a matching ID
async def retrieve_person(id: str) -> dict:
    person = await people_collection.find_one({"_id": ObjectId(id)})
    if person:
        return person_helper(person)


# Update a person with a matching ID
async def update_person(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    person = await people_collection.find_one({"_id": ObjectId(id)})
    if person:
        updated_person = await people_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_person:
            return True
        return False


# Delete a person from the database
async def delete_person(id: str):
    person = await people_collection.find_one({"_id": ObjectId(id)})
    if person:
        await people_collection.delete_one({"_id": ObjectId(id)})
        return True
