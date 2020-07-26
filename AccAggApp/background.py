from background_task import background
from django.contrib.auth.models import User
import requests
from .models import Settings
from AABharatFed import settings


def create_dummy_data(mobile_numberm):

    url='https://sandbox.moneyone.in/developerportalserver_sandbox/api/finproadmin/createMockData'
    headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': 'https://developer.onemoney.in',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://developer.onemoney.in/mainpage/manage-test-data',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6',
    'Host': 'sandbox.moneyone.in',
    'Connection': 'keep-alive',
    'environmentType': 'TEST',
    }
    token=Settings.objects.get(id=1).google_auth_token
    headers['Authorization']=token
    payload={"mobileNumber":mobile_numberm}
    resp=requests.post(url,json=payload,proxies=settings.proxy,verify=False,headers=headers)
    print('BACKGROUND',resp.text)