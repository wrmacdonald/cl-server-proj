from flask_testing import TestCase
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

