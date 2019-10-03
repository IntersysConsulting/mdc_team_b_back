from flask import jsonify
from flask_restplus import Resource
from ...db import Database
from pymongo import errors
from .schema import CustomerSchema
from datetime import datetime
from ..password_management import hash_password, verify_hash
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required)
from bson.objectid import ObjectId
from ..validation import is_guest, is_customer, is_customer_email_available
from copy import deepcopy

class CustomerManager():
    def __init__(self):
        self.collection_name = "customers"
        self.db = Database()

    def make_guest(self):
        new_user = {"is_guest": True}
        result = self.db.create(self.collection_name, new_user)
        return result

    #region Customer Data

    def create_new_customer(self, _id, first_name, last_name, email, password,
                            phone):
        now = datetime.now()
        # _id = get_jwt_identity()
        print("An account is trying to be created with the id: {}".format(_id))
        try:
            is_user_guest = self.db.find(self.collection_name, {
                "_id": ObjectId(_id),
                "is_guest": True
            })
            if is_user_guest:
                email_is_available = is_customer_email_available(email)
                if email_is_available:
                    new_user = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "password": hash_password(password),
                        "phone": phone,
                        "terms_of_service_ts": now,
                        "is_guest": False,
                        "shipping_addresses": [],
                        "billing_addresses": []
                    }

                    print("Making this new user: {}".format(new_user))
                    result = self.db.update(self.collection_name,
                                            {"_id": ObjectId(_id)},
                                            {"$set": new_user})
                    # result = self.db.create(self.collection_name, new_user)
                    print("The database returned: {}".format(result))
                    result = 1

                else:
                    result = -1
            else:
                result = -2
        except:
            result = 0
        return result

    def login(self, email, password):
        '''
        Attempts to log in an customer. 
        Returns  1, _id  on Success (_id = customer object id)
        Returns  0, None on Wrong Password
        Returns -1, None on Wrong Email

        Keyword arguments:
        email -- The email of the customer
        password -- The password of the customer
        '''

        result = self.db.find(self.collection_name, {
            "email": email,
            "is_guest": False
        })

        if result == None:
            response = (-1, None)
        else:
            customer = self.dump(result)
            response = (1, customer["_id"]) if verify_hash(
                password, customer["password"]) else (0, None)

        return response

    def update_info(self,
                    _id,
                    first_name=None,
                    last_name=None,
                    email=None,
                    phone=None):
        if is_guest(_id):
            if (first_name == None or last_name == None or email == None):
                # Guest must not leave any of these blank
                response = -1

            else:
                # Guest can update their account
                email_valid = is_customer_email_available(email)

        elif is_customer(_id):
            # The customer can update their account
            email_valid = True if email == None else is_customer_email_available(
                email, _id)

        else:
            # This is not a person we can update
            response = -2

        # If there is a non-guest customer that already has that email...

        if email_valid:
            update_fields = {}
            if first_name != None:
                update_fields["first_name"] = first_name
            if last_name != None:
                update_fields["last_name"] = last_name
            if email != None:
                update_fields["email"] = email
            if phone != None:
                update_fields["phone"] = phone

            print("Updating {} with {}".format(_id, update_fields))

            response = self.db.update(self.collection_name,
                                      {"_id": ObjectId(_id)},
                                      {"$set": update_fields})
        elif not email_valid:
            # If the email is taken already
            response = -3

        return response

    def get_data(self, _id):
        return self.dump(self.db.find(self.collection_name,
                                      {"_id": ObjectId(_id)}),
                         only_personal=True)

    #endregion

    #region Generic Address
    def add_address(self, user_id, array, new_address, is_default):
        #expects billing_addresses or shipping_addresses on array
        customer = self.db.find(self.collection_name,
                                {"_id": ObjectId(user_id)})

        if customer == None:
            #Customer does not exist
            response = -1
        else:

            if array in customer.keys():
                addresses = [x for x in customer[array]]
            else:
                addresses = []

            if new_address in addresses:
                # Duplicate
                response = -2
            elif is_default and len(addresses) > 0:
                address_to_be_pushed = addresses[-1]
                result = self.db.update(
                    self.collection_name, {"_id": ObjectId(user_id)},
                    {"$push": {
                        array: address_to_be_pushed
                    }})
                if result == 1:
                    # Replace the old default with the new one
                    response = self.db.update(
                        self.collection_name, {"_id": ObjectId(user_id)},
                        {"$set": {
                            "{}.0".format(array): new_address
                        }})
                    # Should undo the damage if something fails here
                else:
                    # Could not replace
                    response = -3
            else:
                response = self.db.update(self.collection_name,
                                          {"_id": ObjectId(user_id)},
                                          {"$push": {
                                              array: new_address
                                          }})
        return response
    def make_address(self, address, between, country, state, city, zip_code,
                     first_name, last_name, delivery_notes):
        new_fields = {}
        if address:
            new_fields["address"] = address
        if between:
            new_fields["between"] = between
        if country:
            new_fields["country"] = country
        if state:
            new_fields["state"] = state
        if city:
            new_fields["city"] = city
        if zip_code:
            new_fields["zip_code"] = zip_code
        if first_name:
            new_fields["first_name"] = first_name
        if last_name:
            new_fields["last_name"] = last_name
        if delivery_notes:
            new_fields["delivery_notes"] = delivery_notes
        return new_fields
    def update_address(self, user_id, array, new_fields, index, is_default):
        '''
        Updates an address generically.
        Returns 1 on Success, 0 on Failure, -1 On Not a customer, -2 on IndexOutOfArrayRange 
        '''
        customer = self.get_data(user_id)
        if customer == None:
            # Customer does not exist
            can_update = False
            response = -1
        else:
            addresses = customer[array]
            if(index>len(addresses)-1):
                # Index out of range
                response = -2
            else:
                if is_default and not index == 0:
                    # Swaps out the updated address with 0 (is_default) and sets to update on 0
                    # Deepcopy Allows us to copy actual objects instead of references. If you don't do this then both objects will be changed.
                    tmp_address = deepcopy(addresses[0])
                    addresses[0] = deepcopy(addresses[index])
                    addresses[index] = tmp_address
                    index_to_update = 0
                else:  #is_default == False or  ( index == 0 and is_default == True )
                    # The address can be changed directly
                    index_to_update = index

                # Checks every field to be updated
                for key in new_fields.keys():
                    addresses[index_to_update][key] = new_fields[key]

                response = self.db.update(self.collection_name, {"_id":ObjectId(user_id)}, {"$set":{array:addresses}})

        return response
    #endregion

    def add_billing(self, user_id, address, country, state, city, zip_code,
                    first_name, last_name, is_default):

        new_address = self.make_address(address, None, country, state, city,
                                   zip_code, first_name, last_name,
                                   None)
        return self.add_address(user_id, "billing_addresses", new_address,
                                is_default)

    def update_billing(self, user_id, index, address, country, state, city,
                       zip_code, first_name, last_name, is_default):
        new_fields = self.make_address(address, None, country, state, city,
                                       zip_code, first_name, last_name, None)
        return self.update_address(user_id, "billing_addresses", new_fields, index, is_default)


    def delete_billing(self, user_id, billing_obj_id):
        pass

    def add_shipping(self, user_id, address, between, country, state, city,
                     zip_code, first_name, last_name, delivery_notes,
                     is_default):

        new_address = self.make_address(address, between, country, state, city,
                                   zip_code, first_name, last_name,
                                   delivery_notes)
        return self.add_address(user_id, "shipping_addresses", new_address,
                                is_default)




    def update_shipping(self, user_id, index, address, between, country, state, city,
                     zip_code, first_name, last_name, delivery_notes,
                     is_default):
        new_fields = self.make_address(address, between, country, state, city,
                                       zip_code, first_name, last_name, delivery_notes)
        return self.update_address(user_id, "shipping_addresses", new_fields,
                                   index, is_default)

    def delete_shipping(self, user, shipping_obj_id):
        pass

    def dump(self, data, only_personal=False):
        _personal_data_exclusion = [
            '_id', 'password', 'terms_of_service_ts', 'is_guest'
        ] if only_personal else []
        return CustomerSchema(exclude=_personal_data_exclusion).dump(data).data