from flask_testing import TestCase

from app import app, db, jsonify

class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite:///tests.db"
    TESTING = True

    def create_app(self):
 
        # pass in test configuration
        
        return app

    def setUp(self):
        db.init_app(app)
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # @app.route("/")
    # def some_json():
    #     return jsonify(success=True)


    def test_some_json(self):
        response = self.client.get("/")
        self.assertEqual(response.json, dict(msg="Hello Api"))

    # def test_login(self):
    #     response= self.client.post("/login", data={"username":"kowal20x7","password":"kabanos1"},content_type='application/json')
    #     self.assertEqual(response.status_code, 200)

    # def test_posts(self):
    #     response= self.client.get("/post")
    #     self.assertEqual(response.status_code, 200)

import unittest
import flask_testing

# your test cases

if __name__ == '__main__':
    unittest.main()