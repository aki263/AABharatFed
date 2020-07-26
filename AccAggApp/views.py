import datetime
import json
import time
import uuid
from AABharatFed import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import make_req
import websocket
from django.shortcuts import render, redirect
from django.views import View
import requests
from .models import *



# Create your views here.


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        try:

            profile = Profile.objects.get(user=request.user)
            if profile.profile_complete is True:
                return redirect('/accounts/dashboard/')
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




            return render(request, 'profilec.html', {'login': acc,'dashboard':resp.json(),'username':request.user})

        except Exception as ex:
            print(ex)
            return render(request, 'profilec.html', {'login': 'acc created','dashboard':''})

    def post(self,request):
        profile = Profile.objects.get(user=request.user)
        profile.profile_complete=True
        profile.save()
        return redirect('/accounts/dashboard/')



def make_req_with_session(url,payload,sessionid):

    headers={'sessionId':sessionid}
    resp = requests.post(url, json=payload, verify=False, proxies=settings.proxy,headers=headers)
    return  resp


class Conset1(LoginRequiredMixin,View):
    def get(self,request):
        profile=Profile.objects.get(user=request.user)
        txnid=str(uuid.uuid4())
        current_dt=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        exp_dt=datetime.datetime(year=2020,month=12,day=30).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        client_api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ik5PTjAyMjIiLCJ0eXBlIjoiRklVIiwiaWF0IjoxNTk1MDkzNjcyLCJleHAiOjE2MTIzNzM2NzJ9.0SWWl4OgPobDleuHkeaQKmRkMojqiD97KWWzeN4vRT4'
        url='https://api-sandbox.onemoney.in/aa/Consent'
        payload={
                  "ver": "1.1.3",
                  "timestamp": current_dt,
                  "txnid": "4a4adbbe-29ae-11e8-a8d7-0289437bf331",
                  "ConsentDetail": {
                    "consentStart": current_dt,
                    "consentExpiry": exp_dt,
                    "consentMode": "VIEW",
                    "fetchType": "ONETIME",
                    "consentTypes": [
                      "TRANSACTIONS",
                      "PROFILE",
                      "SUMMARY"
                    ],
                    "fiTypes": [
                      "DEPOSIT"
                    ],
                    "DataConsumer": {
                      "id": "finprobank"
                    },
                    "Customer": {
                      "id": "9910423393@onemoney"
                    },
                    "Purpose": {
                      "code": "101",
                      "refUri": "https://api.rebit.org.in/aa/purpose/101.xml",
                      "text": "Wealth management service",
                      "Category": {
                        "type": "string"
                      }
                    },
                    "FIDataRange": {
                      "from": current_dt,
                      "to": exp_dt
                    },
                    "DataLife": {
                      "unit": "MONTH",
                      "value": 1
                    },
                    "Frequency": {
                      "unit": "MONTH",
                      "value": 1
                    }

                  }
                }

        headers={'client_api_key':client_api_key}
        resp=requests.post(url,json=payload,verify=False, proxies=settings.proxy,headers=headers)

        print(resp.json())
        ConsentHandle=resp.json()['ConsentHandle']
        headers={
            'sessionId':profile.sessionid
        }
        url='https://api-sandbox.onemoney.in/app/otp/send'
        payload={
            'actionType':'CONSENT_CONFIRMED',
            'identifierValue':'9910423393',
            "identifierType": "MOBILE"
        }
        resp = requests.post(url, json=payload, verify=False, proxies=settings.proxy, headers=headers)
        payload={
                "consentHandles" :[ConsentHandle ],
                "otp": "123456",
                    "accounts": [{
                        "type": "BANK",
                        "data": {
                            "accType":"SAVINGS",
                            "accRefNumber" : "1ff001af-a591-4d29-9c08-689f6a222376",
                            "maskedAccNumber": "XXXXXXXXXX4714",
                            "fipId": "finsharebank",
                            "userInfo": {}
                        }
                    },
                    ]
                }
        url = 'https://api-sandbox.onemoney.in/sdk/api/v1/consentwithauth/allow'
        resp=requests.post(url,json=payload, verify=False, proxies=settings.proxy, headers=headers)
        print(resp)

        return render(request, 'consent1.html', {'login': 'Added Succeess'})

class profile2(View):
    def get(self,request):
        return render(request, 'profilec.html', {'login': 'Added Succeess'})

    def post(self,request):
        return redirect('/accounts/dashboard/')

class Dashboard(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'dashboard.html', {'user':request.user, 'first_name':request.user.first_name,'last_name':request.user.last_name,
                                                 'first_name_letter': str(request.user.first_name[:1]).upper(),
                                                 'full_name': request.user.first_name +' '+request.user.last_name,'noti_msg':'3'} )

    def post(self,request):
        return redirect('/accounts/dashboard/')

class Expense(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'expense.html', {'user':request.user, 'first_name':request.user.first_name,'last_name':request.user.last_name,
                                                 'first_name_letter': str(request.user.first_name[:1]).upper(),
                                                 'full_name': request.user.first_name +' '+request.user.last_name,'noti_msg':'3'} )

    def post(self,request):
        return render(request, 'expense.html',
                      {'user': request.user, 'first_name': request.user.first_name, 'last_name': request.user.last_name,
                       'first_name_letter': str(request.user.first_name[:1]).upper(),
                       'full_name': request.user.first_name + ' ' + request.user.last_name, 'noti_msg': '3'})