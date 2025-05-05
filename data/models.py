import pymongo
import os

client = pymongo.MongoClient(os.environ.get('MONGO_CONN_STRING', None))

def addPortfolio(portfolio_name, portfolio):
    col = client["portfolio"]
    col.find_one_and_update({"user_email": user_email, "name": portfolio_name}, {"$set": portfolio}, upsert=True)

# get the user or create a new user if one does not exist and return the user
def addOrUpdateUser(user): 
    db = client["portfolio"]
    user_collection = db["users"]
    user = user_collection.find_one_and_update({"email": user["email"]}, {"$set": user}, upsert=True)
    #print("addOrUpdateUser", user)  
    return user    

