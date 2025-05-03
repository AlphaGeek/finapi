import pymongo
import os

client = pymongo.MongoClient(os.environ.get('MONGO_CONN_STRING', None))

def addPortfolio(portfolio_name, portfolio):
    col = client["Portfolios"]
    col.find_one_and_update({"user_email": user_email, "name": portfolio_name}, {"$set": portfolio}, upsert=True)

# get the user or create a new user if one does not exist and return the user
def addOrUpdateUser(user): 
    col = client["Users"]
    user = col.find_one_and_update({"email": user["email"]}, {"$set": user}, upsert=True)
    return user    

