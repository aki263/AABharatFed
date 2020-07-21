import datetime
import json
import time
import uuid
from .forms import make_req
import websocket
from django.shortcuts import render
from django.views import View
import requests
from .models import *



# Create your views here.


class ProfileView(View):

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        mobile=profile.mobile
        sessionid=profile.sessionid
        base_url='https://api-sandbox.onemoney.in'

        #discover
        payload={"fipID":"finsharebank","fips":[{"data":[{"type":"MOBILE","value":mobile}]}]}
        resp=make_req_with_session(base_url+'/app/accounts/discover',payload,sessionid)
        acc=resp.json()['DiscoveredAccounts']
        print('DISCOVER RESPONSE',resp)

        #link accounts
        for i in range(0,len(acc)):
            acc[i]['linkRequested']=True

        print(acc)
        payload= {'discoveredAccounts':acc,"fip":{"FIPName":"Universal Bank","FIPID":"finsharebank"}}
        resp=make_req_with_session(base_url+'/app/accounts/link',payload,sessionid)
        print('LINK RESPONSE',resp.text)
        RefNumber=resp.json()['data']['RefNumber']

        #final otp

        payload={"otp":"123456","RefNumber":RefNumber,"fipID":"finsharebank"}
        resp=make_req_with_session(base_url+'/app/accounts/otp',payload,sessionid)
        print('FINAL OTP RESPONSE', resp.text)

        #dashboard

        resp=requests.get(base_url+'/app/dashboard', headers={'sessionId':sessionid})




        return render(request, 'profile.html', {'login': acc,'dashboard':resp.json()})


    def post(self,request):

        return render(request, 'profile.html', {'login': 'Added Succeess'})



def make_req_with_session(url,payload,sessionid):
    proxy = {
        'http': 'http://127.0.0.1:8888',
        'https': 'http://127.0.0.1:8888',
    }
    headers={'sessionId':sessionid}
    resp = requests.post(url, json=payload, verify=False, proxies=proxy,headers=headers)
    return  resp