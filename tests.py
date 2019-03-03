import os
import tempfile

import pytest
from app import db,app


class TestApi:

	def test_index(self):
		with app.test_client() as client:
			response=client.get('/')
			print(response.data)
			assert response.status_code==200

	def test_token(self):
		with app.test_client() as client:
			usr='test'
			pswrd='test'
			response=client.post('/login',data='{"username": "test", "password": "test"}', content_type='application/json', charset='UTF-8')
			print(response.get_json())
			assert response.status_code==200


		
		
		
		

        
	
