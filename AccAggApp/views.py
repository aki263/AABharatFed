import datetime
import json
import time
import uuid

import websocket
from django.shortcuts import render
from django.views import View

from .models import *


# Create your views here.


class ProfileView(View):

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        mid = profile.uuid
        mid = str(uuid.uuid4())
        sid = profile.sid
        if profile.banklink == False:
            ws = websocket.WebSocket()
            ws.connect("wss://wssdev.finvu.in/api", http_proxy_host="127.0.0.1", http_proxy_port=8888)
            payload = {'username': request.user.username + '@finvu', 'password': '2468'}
            result = send_wss(ws, 'urn:finvu:in:app:req.login.01', payload, mid)
            result = json.loads(result)
            # print(result)
            sid = result['header']['sid']
            time.sleep(1)

            # user linked accounts
            payload = {'userid': request.user.username + '@finvu'}
            result = json.loads(send_wss(ws, 'urn:finvu:in:app:req.userLinkedAccount.01', payload, mid, sid))
            time.sleep(1)
            payload = {}
            result = json.loads(send_wss('urn:finvu:in:app:req.popularSearch.01', payload, mid, sid))
            time.sleep(1)

            # get bob from list
            txnid = uuid.uuid4()
            profile.txnid = txnid
            profile.save()
            payload = {"ver": "1.0",
                       "timestamp": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                       "txnid": txnid,
                       "Customer": {"id": request.user.username + '@finvu', "Identifiers":
                           [{"category": "STRONG", "type": "MOBILE", "value": profile.mobile}]},
                       "FIPDetails": {"fipId": "BARB0KIMXXX", "fipName": "Bank of Baroda"},
                       "FITypes": ["DEPOSIT"]}
            result = json.loads(send_wss(ws, 'urn:finvu:in:app:req.discover.01', payload, mid, sid))
            time.sleep(1)

            # adding account
            first_account = result['payload']['DiscoveredAccounts'][0]
            payload = {"ver": "1.0",
                       "timestamp": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                       "txnid": txnid,
                       "FIPDetails": {"fipId": "BARB0KIMXXX", "fipName": "Bank of Baroda"},
                       "Customer": {"id": request.user.username + '@finvu',
                                    "Accounts": [{"maskedAccNumber": first_account['maskedAccNumber']
                                                     , "accRefNumber": first_account['accRefNumber'],
                                                  "FIType": first_account['FIType'],
                                                  "accType": first_account['accType']}]}}
            result = json.loads(send_wss(ws, 'urn:finvu:in:app:req.linking.01', payload, mid, sid))
            print(result)

            # {"header":{"mid":"7c6c5c5b-5c23-4fd4-9cce-6426c505ef2c","ts":"2020-07-16T23:42:47.079Z","sid":"01EDD04DVY7TF3KX4RQ6AYCQKP","dup":false,"type":"urn:finvu:in:app:req.discover.01"},"payload":{"ver":"1.0","timestamp":"2020-07-16T23:42:47.079Z","txnid":"24ac6162-ed95-42e2-81cf-4844491da8a6","Customer":{"id":"yyttte@finvu","Identifiers":[{"category":"STRONG","type":"MOBILE","value":"9910423393"}]},"FIPDetails":{"fipId":"BARB0KIMXXX","fipName":"Bank of Baroda"},"FITypes":["DEPOSIT"]}}

        return render(request, 'profile.html', {'login': result})


def login_wss(username, password, mid):
    payload = {'username': username, 'password': '2468'}
    return send_wss('urn:finvu:in:app:req.login.01', payload, mid)


def send_wss(ws, req_type, payload, mid, sid=None):
    msg = {"header": {"mid": str(uuid.uuid4()),
                      "ts": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z', "sid": sid,
                      "dup": False,
                      "type": req_type}, "payload": payload}

    msg = json.dumps(msg)
    print(msg, 'WS FUNC-REQUEST')
    ws.send(msg)
    result = ws.recv()
    print(result, 'WS FUNC-RESPONSE')

    return result
