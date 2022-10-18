from flask import Flask
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy
from app import app, db
import os


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_DATABASE_URL')
        return app

    def setUp(self):
        db.create_all()

    def test_1(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_2(self):
        response = self.client.get('/bad_users')
        self.assertEqual(response.status_code, 404)

    # def test_users_1(self):
    #     response = self.client.get('/users')
    #     app.logger.info(response.data)
    #     self.assertEqual(response.data, [])

    # def test_users_2(self):
    #     test_data = dict(
    #         address='123 Test',
    #         email='unittest.com',
    #         image='www.unit_test-image.com',
    #         name='unittest')
    #     response = self.client.post('/users', data=test_data)
    #     app.logger.info(response.data)
    #     self.assertEqual(response.status_code, 200)
    #     # self.assertEqual(response.data, [])

    def tearDown(self):
        db.session.remove()
        db.drop_all()

