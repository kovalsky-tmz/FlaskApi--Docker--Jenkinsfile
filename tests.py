import os
import tempfile

import pytest
from app import db,app
from models import Post,User
from werkzeug.security import generate_password_hash, \
     check_password_hash

@pytest.fixture(scope='module')
def get_token():
	with app.test_client() as client:
		usr='test'
		pswrd='test'
		response=client.post('/login',json={"username": usr, "password": pswrd}, content_type='application/json', charset='UTF-8')
		print(response.get_json())
		return response.get_json()['access_token']

class TestApi:

	def setup_method(self, method):
		post=Post(title='ttil',content='cont',user_id=1)
		db.session.add(post)
		db.session.flush()

	def test_index(self):
		with app.test_client() as client:
			response=client.get('/')
			print(response.data)
			assert response.status_code==200

	def test_token(self):
		with app.test_client() as client:
			usr='test'
			pswrd='test'
			response=client.post('/login',json={"username": usr, "password": pswrd}, content_type='application/json', charset='UTF-8')
			print("Testing token, response: ", response.get_json())
			assert response.status_code==200

	def test_newuser(self,get_token):
		with app.test_client() as client:
			username="test1"
			password="test"
			response=client.post('/users',json={"username": username, "password": password, "auth_token": get_token}, content_type='application/json', charset='UTF-8')
			pass_hash = generate_password_hash(password)
			user=User(username=username,password=pass_hash)
			db.session.add(user)
			db.session.flush()
			assert User.query.filter_by(username='test1').count()>0


	def teardown_method(self, method):
		db.session.rollback()
		db.session.remove()
		
		
		
		

        
	
