import requests
import pytest
def test_email_name():
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2YTY5YmVlODU5M2Q5MTAwM2Q1MzRiMTIiLCJpYXQiOjE3ODc2NDYwODksImV4cCI6MTc4ODI1MDg4OX0.xxaLrTGM78LROfOk7pje4WNAL8Jd9ld8a-2075WGgr8'
    response = requests.get('https://qa-mesto.praktikum-services.ru/api/users/me',
                            headers = {'Authorization': token})
    r = response.json()['data']['email']
    assert r == 'sarapulov_51@ya.ru'

test_email_name()