import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from main import app
from app.database.model.schema import base
from app.database.config.connect import getdb
from app.helpers.hashing import Hash

dburl = "sqlite:///{}".format(os.path.join(os.path.dirname(__file__), 'test.db'))
engine_test = create_engine(dburl, connect_args={"check_same_thread": False})
session_test = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)
base.metadata.create_all(bind=engine_test)

client = TestClient(app)
test_user_url = '/user'
test_auth_url = '/auth/login'

def insert_user():
  passwordhash = Hash.password('testpassword')
  connection = engine_test.connect();
  connection.execute(text(f"INSERT INTO user (username, password, firstname, lastname, address, phone, email, status) VALUES ('testusername', '{passwordhash}', 'test first name', 'test lastname', 'test address', '3210000000', 'testemail@gmail.com', 'true' )"))
  connection.commit()

insert_user()

def override_getdb():
  db = session_test()
  try:
    yield db
  finally:
    db.close()

app.dependency_overrides[getdb] = override_getdb

def test_create_user():
  user = {
    "username": "testusername2",
    "password": "testpassword2",
    "firstname": "test firstname 2",
    "lastname": "test lastname 2",
    "address": "test address 2",
    "phone": "3210000001",
    "email": "testemail2@gmail.com"
  }
  
  user_create_unauthorize = client.post(test_user_url, json=user)
  assert user_create_unauthorize.status_code == 401
  
  auth = {"username": "testusername", "password": "testpassword"}
  auth_response = client.post(test_auth_url, data=auth)
  assert auth_response.status_code == 200
  assert auth_response.json()["token_type"] == "bearer"
  
  headers = { 'Authorization': f'Bearer {auth_response.json()["access_token"]}' }
  user_create_response = client.post(test_user_url, json=user, headers=headers)
  assert user_create_response.status_code == 201
  assert user_create_response.json()["message"] == "Registro creado correctamente."
  

def test_getall_user():
  auth = {'username': 'testusername', 'password': 'testpassword'}
  auth_response = client.post(test_auth_url, data=auth)
  assert auth_response.status_code == 200
  assert auth_response.json()["token_type"] == "bearer"
  
  headers = { 'Authorization': f'Bearer {auth_response.json()["access_token"]}' }
  user_getall_response = client.get(test_user_url, headers=headers)
  assert user_getall_response.status_code == 200
  assert len(user_getall_response.json()) == 2
  
def test_getbyid_user():
  auth = {'username': 'testusername', 'password': 'testpassword'}
  auth_response = client.post(test_auth_url, data=auth)
  assert auth_response.status_code == 200
  assert auth_response.json()["token_type"] == "bearer"
  
  headers = { 'Authorization': f'Bearer {auth_response.json()["access_token"]}' }
  user_getbyid_response = client.get(f"{test_user_url}/1", headers=headers)
  assert user_getbyid_response.status_code == 200
  assert user_getbyid_response.json()["username"] == "testusername"
  
  
def test_delete_user():
  auth = {'username': 'testusername', 'password': 'testpassword'}
  auth_response = client.post(test_auth_url, data=auth)
  assert auth_response.status_code == 200
  assert auth_response.json()["token_type"] == "bearer"
  
  headers = { 'Authorization': f'Bearer {auth_response.json()["access_token"]}' }
  user_delete_response = client.delete(f"{test_user_url}/2", headers=headers)
  assert user_delete_response.status_code == 200
  assert user_delete_response.json()["message"] == "Registro eliminado correctamente."
  
  user_delete_getbyid_response = client.get(f"{test_user_url}/2", headers=headers)
  assert user_delete_getbyid_response.status_code == 404
  assert user_delete_getbyid_response.json()["message"] == "No se encontro el registro."
  
  
def test_update_user():
  auth = {'username': 'testusername', 'password': 'testpassword'}
  auth_response = client.post(test_auth_url, data=auth)
  assert auth_response.status_code == 200
  assert auth_response.json()["token_type"] == "bearer"
  
  user = { "username": "testusernameupdate" }
  headers = { 'Authorization': f'Bearer {auth_response.json()["access_token"]}' }
  
  user_update_response = client.put(f"{test_user_url}/1", json=user, headers=headers)
  assert user_update_response.status_code == 200
  assert user_update_response.json()["message"] == "Registro actializado correctamente."
  
  user_getbyid_response = client.get(f"{test_user_url}/1", headers=headers)
  assert user_getbyid_response.status_code == 200
  assert user_getbyid_response.json()["username"] == "testusernameupdate"
  assert user_getbyid_response.json()["firstname"] == "test first name"
  
def test_update_notfound_user():
  auth = {'username': 'testusernameupdate', 'password': 'testpassword'}
  auth_response = client.post(test_auth_url, data=auth)
  assert auth_response.status_code == 200
  assert auth_response.json()["token_type"] == "bearer"
  
  user = { "username": "testusernameupdatenotfound" }
  headers = { 'Authorization': f'Bearer {auth_response.json()["access_token"]}' }
  
  user_update_notfound_response = client.put(f"{test_user_url}/2", json=user, headers=headers)
  assert user_update_notfound_response.status_code == 404
  assert user_update_notfound_response.json()["message"] == "No se encontro el registro."
  
def test_delete_notfound_user():
  auth = {'username': 'testusernameupdate', 'password': 'testpassword'}
  auth_response = client.post(test_auth_url, data=auth)
  assert auth_response.status_code == 200
  assert auth_response.json()["token_type"] == "bearer"
  
  headers = { 'Authorization': f'Bearer {auth_response.json()["access_token"]}' }
  user_delete_notfound_response = client.delete(f"{test_user_url}/2", headers=headers)
  assert user_delete_notfound_response.status_code == 404
  assert user_delete_notfound_response.json()["message"] == "No se encontro el registro."
  
  
def test_delete_database():
  engine_test.dispose()
  dbsqlite = os.path.join(os.path.dirname(__file__), 'test.db')
  os.remove(dbsqlite)