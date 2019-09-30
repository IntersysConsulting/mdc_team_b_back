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


def is_customer_email_available(email, _id=None):
    '''
    Returns true if:
        The email is not assigned to any non-guest accounts
        The email matches the _id provided
    '''
    if _id == None:
        # If the email doesn't belong to any non-guest customer
        selector = {"email": email, "is_guest": False}
        expected = True
    else:
        # If the email matches the ID of the customer asking
        selector = {"email": email, "_id": _id}
        expected = False
    return (db.find("customers", selector) == None) == expected


is_not_guest_response = {"statusCode": 403, "message": "User is not guest."}

is_not_customer_response = {
    "statusCode": 403,
    "message": "User is not customer."
}

is_not_admin_response = {"statusCode": 403, "message": "User is not admin."}
