from ...db import Database
from bson.objectid import ObjectId
db = Database()


def is_guest(_id):
    return db.find("customers", {
        "_id": ObjectId(_id),
        "is_guest": True
    }) != None


def is_customer(_id):
    return db.find("customers", {
        "_id": ObjectId(_id),
        "is_guest": False
    }) != None


def is_admin(_id):
    return db.find("admins", {"_id": ObjectId(_id)}) != None


is_not_guest_response = {"statusCode": 403, "message": "User is not guest."}

is_not_customer_response = {
    "statusCode": 403,
    "message": "User is not customer."
}

is_not_admin_response = {"statusCode": 403, "message": "User is not admin."}
