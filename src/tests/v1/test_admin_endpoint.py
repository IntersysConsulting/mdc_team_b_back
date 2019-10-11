from flask_jwt_extended import JWTManager
from jwt import exceptions
from flask_mail import Mail
from flask import jsonify

import urllib.parse
import unittest
import requests
import random
import string
import json
import time
import os

import requests

from app import create_app
from jwtholder import (app, mail)

class AdminEndPointResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        
    def make_post(self, email, password):
        return self.client.post('http://127.0.0.1:5000/api/v1/admin/session/', data=urllib.parse.urlencode({
            'email':email,
            'password':password
        }), content_type='application/x-www-form-urlencoded')

    def make_delete(self, token):
        return self.client.delete('http://127.0.0.1:5000/api/v1/admin/session/', headers={
            'Authorization' : 'Bearer {}'.format(token)
        })
    
    def make_put(self, token):
        return self.client.put('http://127.0.0.1:5000/api/v1/admin/session/', headers={
            'Authorization' : 'Bearer {}'.format(token)
        })

    def test_post(self):
        ''' Test for post method of the admin/session endpoint '''
        # Access token 
        response = json.loads(self.make_post('bear@bear.com', 'bear').data.decode('utf-8'))
        if response['access_token'] is None:
            raise AssertionError('Login response for this test should be a valid access token')

        # Positive response
        response = json.loads(self.make_post('bear@bear.com', 'bear').data.decode('utf-8'))
        if response['statusCode'] is not 200:
            raise AssertionError('Login response for this test should be 200')

        # Negative response 
        response = json.loads(self.make_post('wrong@wrong.com', 'bear').data.decode('utf-8'))
        if response['statusCode'] is 400:
            raise AssertionError('Login response for this test should be 400')

        # Negative response, empty email
        response = json.loads(self.make_post('', 'bear').data.decode('utf-8'))
        if response['statusCode'] is 400:
            raise AssertionError('Login response for this test should be 400')

        # Negative response, empty password
        response = json.loads(self.make_post('wrong@wrong.com', '').data.decode('utf-8'))
        if response['statusCode'] is 400:
            raise AssertionError('Login response for this test should be 400')

    def test_delete(self):
        ''' Test for delete method of the admin/session endpoint '''
        # Positive response
        access_token = json.loads(self.make_post('bear@bear.com', 'bear').data.decode('utf-8'))['access_token']
        token_len = len(access_token)
        response = json.loads(self.make_delete(access_token).data.decode('utf-8'))
        if response['statusCode'] is not 200:
            raise AssertionError('Logout response for this test should be 200')

        # Negative response
        fake_token =  ''.join(random.choices(string.ascii_letters + string.digits, k=token_len))
        response = json.loads(self.make_delete(fake_token).data.decode('utf-8'))
        if 'Not enough segments' not in response['msg'] :
            raise AssertionError('Logout response for this test should be Not enough segments due to the invalid token')
        # Negative response
        try:
            response = json.loads(self.make_delete('').data.decode('utf-8'))
            raise AssertionError('Logout response for this test should be Not enough segments due to the invalid token')
        except:
            pass

    def test_put(self):
        ''' Test for put method of the admin/session endpoint '''
        # Positive response
        refresh_token = json.loads(self.make_post('bear@bear.com', 'bear').data.decode('utf-8'))['refresh_token']
        token_len = len(refresh_token)
        response = json.loads(self.make_put(refresh_token).data.decode('utf-8'))
        if response['statusCode'] is not 200:
            raise AssertionError('Token refresh response for this test should be 200')
            
        fake_token =  ''.join(random.choices(string.ascii_letters + string.digits, k=token_len))
        response = json.loads(self.make_put(fake_token).data.decode('utf-8'))
        
        if 'Not enough segments' not in response['msg'] :
            raise AssertionError('Token refresh response for this test should be Not enough segments due to the invalid token')