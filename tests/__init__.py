from unittest.mock import ANY

from flask import url_for
from flask_bcrypt import Bcrypt
from flask_testing import TestCase
import unittest
from app import app
from app.db import engine, metadata

class BaseTestCase(TestCase):
    def create_app(self):
        app.testing = True
        self.app = app.test_client()
        return app

    def setUp(self):
        super().setUp()
        self.create_app()
        metadata.drop_all(engine)
        metadata.create_all(engine)
        self.calculator1 = {
            "name": "Area of rectangle",
            "description": "Calculates the area of a rectangle.",
            "inputData": "matrix -size=(1,4) -type=integer",
            "code": "string",
            "isPublic": True
        }
        self.review1 = {
            "rating": 5,
            "message": "This is a comment"
        }
        self.user1 = {
            "email": "oleksandr.yovbak@gmail.com",
            "username": "probablyskela",
            "password": "ASDaejfaslfaSFjlasf",
            "role": "User"
        }
        self.user1login = {"username": "probablyskela", "password": "ASDaejfaslfaSFjlasf"}
        self.user2 = {
            "email": "bohdan7nava@gmail.com",
            "username": "roflanmen",
            "password": "123456",
            "role": "User"
        }
        self.user2login = {"username": "roflanmen", "password": "123456"}
        self.admin = {
            "email": "1@gmail.com",
            "username": "admin",
            "password": "123456",
            "role": "Admin"
        }
        self.adminlogin = {"username": "admin", "password": "123456"}
        
    def tearDown(self):
        super().tearDown()
        metadata.drop_all(engine)

