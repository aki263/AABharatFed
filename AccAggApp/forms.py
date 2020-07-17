import datetime
import json
import random
import string
import uuid
from xml.etree.ElementTree import Element, SubElement, tostring

import requests
import websocket
from allauth.account.forms import SignupForm
from allauth.account.signals import user_signed_up
from django import forms
from django.dispatch import receiver

from .models import *


@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    print(user)
    detail_dict = {
        'pan': request.POST.get('pan'),
        'email': request.POST.get('email'),
        'mobile': request.POST.get('mobile'),
    }
    detail_dict = add_user_test_acc(detail_dict)
    profile = Profile.objects.get(user=user)
    profile.accountNo = detail_dict['accountNo']
    profile.accountRefNo = detail_dict['accountRefNo']
    mid = str(uuid.uuid4())
    profile.uuid = mid
    profile.save()
    ws = websocket.WebSocket()
    ws.connect("wss://wssdev.finvu.in/api", http_proxy_host="127.0.0.1", http_proxy_port=8888)
    msg = {"header": {"mid": mid
        , "ts": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z', "sid": None,
                      "dup": False, "type": "urn:finvu:in:app:req.register.01"},
           "payload": {"mobileno": detail_dict['mobile'], "username": user.username + "@finvu", "password": "2468",
                       "repassword": "2468"}}
    msg = json.dumps(msg)
    print(msg)
    ws.send(msg)
    result = ws.recv()
    print(result)
    if 'User account registered' in result:
        # login
        msg = {"header": {"mid": mid, "ts": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                          "sid": None,
                          "dup": False, "type": "urn:finvu:in:app:req.login.01"},
               "payload": {"username": user.username + "@finvu", "password": "2468"}}

        msg = json.dumps(msg)  # error here
        print(msg)
        ws.send(msg)
        result = ws.recv()
        print(result)
        result = json.loads(result)
        sid = result['header']['sid']
        profile.sid = sid
        profile.save()
        if result['payload']['status'] == 'SUCCESS':
            msg = {"header": {"mid": mid, "ts": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                              "sid": sid,
                              "dup": False, "type": "urn:finvu:in:app:req.mobileVerification.01"},
                   "payload": {"mobileNum": detail_dict['mobile']}}

            ws.send(json.dumps(msg))
            result = ws.recv()
            print(result)
            result = json.loads(result)


class MyCustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    mobile = forms.CharField(max_length=10, label='Mobile Number')
    pan = forms.CharField(max_length=11, label='PAN Number')

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)
        mobilec = self.cleaned_data['mobile']
        panc = self.cleaned_data['pan']
        Profile.objects.create(mobile=mobilec, user=user, pan=panc)

        # Add your own processing here.

        # You must return the original result.
        return user


def add_user_test_acc(detail_dict):
    req_api = 'http://api.finvu.in/Accounts/add'

    req = {

        "body": {
            'UserAccountInfo': {
                "UserAccount": {
                    "accountNo": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
                    "accountRefNo": ''.join(random.choices(string.ascii_uppercase + string.digits, k=11)),
                    "accountTypeEnum": 'CURRENT',
                    "FIType": 'DEPOSIT',
                    "Identifiers": {

                        "pan": detail_dict['pan'],
                        "mobile": detail_dict['mobile'],
                        "email": detail_dict['email'],
                        "aadhar": ''.join(random.choices(string.digits, k=10))
                    }
                }
            }
        }

    }

    top = Element('UserAccountInfo')
    useraccount = SubElement(top, 'UserAccount',
                             {'accountRefNo': req['body']['UserAccountInfo']['UserAccount']['accountRefNo'],
                              'accountNo': req['body']['UserAccountInfo']['UserAccount']['accountNo'],
                              'accountTypeEnum': req['body']['UserAccountInfo']['UserAccount']['accountTypeEnum'],
                              'FIType': req['body']['UserAccountInfo']['UserAccount']['FIType']})
    identifier = SubElement(useraccount, 'Identifiers',
                            {'pan': req['body']['UserAccountInfo']['UserAccount']['Identifiers']['pan'],
                             'mobile': str(req['body']['UserAccountInfo']['UserAccount']['Identifiers']['mobile']),
                             'email': req['body']['UserAccountInfo']['UserAccount']['Identifiers']['email'],
                             'aadhar': req['body']['UserAccountInfo']['UserAccount']['Identifiers']['aadhar']})

    Headers = {'Content-type': 'application/xml'}

    detail_dict['accountRefNo'] = req['body']['UserAccountInfo']['UserAccount']['accountRefNo']
    detail_dict['accountNo'] = req['body']['UserAccountInfo']['UserAccount']['accountNo']
    detail_dict['pan'] = req['body']['UserAccountInfo']['UserAccount']['Identifiers']['pan']
    detail_dict['aadhar'] = req['body']['UserAccountInfo']['UserAccount']['Identifiers']['aadhar']

    r = requests.post(req_api, data=tostring(top), headers=Headers)
    print(r.text)

    return detail_dict

# def add_transactions_data(number, start_day, data_dict):
#     # print(number)
#     trans_api = "http://api.finvu.in/Accounts/Transaction/add"
#     start = datetime.strptime(start_day, "%Y-%m-%d")
#     draw_limit = 10000
#     summary = {"currentBalance": round(random.randrange(2000, 20000), 2),
#                "currency": "INR",
#                "exchngeRate": "5.5",
#                "balanceDateTime": str(datetime.combine(start, datetime.min.time())).replace(" ", "T"),
#                "type": "CURRENT",
#                "branch": "Bangalore",
#                "facility": "CC",
#                "ifscCode": "BARBOSHIPOO",
#                "micrCode": "411012011",
#                "openingDate": start_day,
#                "currentODLimit": "20000",
#                "drawingLimit": str(draw_limit),
#                "status": "Active"}
#
#     summary_str = '<Summary currentBalance="{}" currency="{}" exchgeRate="{}" ' \
#                   'balanceDateTime="{}" type="{}" branch="{}" facility="{}" ' \
#                   'ifscCode="{}" micrCode="{}" openingDate="{}" currentODLimit="{}" ' \
#                   'drawingLimit="{}" status="ACTIVE"><Pending amount="20.0"/></Summary> '.format(summary["currentBalance"],
#                                                                                                summary["currency"],
#                                                                                                summary["exchngeRate"],
#                                                                                                summary["balanceDateTime"],
#                                                                                                summary["type"],
#                                                                                                summary["branch"],
#                                                                                                summary["facility"],
#                                                                                                summary["ifscCode"],
#                                                                                                summary["micrCode"],
#                                                                                                summary["openingDate"],
#                                                                                                summary["currentODLimit"],
#                                                                                                summary["drawingLimit"],
#                                                                                                summary["status"])
#
#     c_data_str = '<![CDATA[<Account xmlns="http://api.rebit.org.in/FISchema/deposit" ' \
#                  'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
#                  'xsi:schemaLocation="http://api.rebit.org.in/FISchema/deposit ../FISchema/deposit.xsd" ' \
#                  'linkedAccRef="{}" maskedAccNumber="{}" version="1.0" ' \
#                  'type="deposit"><Profile><Holders type="JOINT"><Holder name="YOUR NAME" dob="1995-04-19" ' \
#                  'mobile="{}" nominee="NOT-REGISTERED" email="{}" pan="{}" ' \
#                  'ckycCompliance="true"/></Holders></Profile> '.format(data_dict['accountRefNo'],
#                                                                        data_dict['accountNo'],
#                                                                        data_dict['phone'],
#                                                                        data_dict['email'],
#                                                                        data_dict['pan'])
#
#     end_str = '</Transactions></Account>]]>'
#
#     transactions = []
#
#     for day in range(number):
#         try:
#             transactions.append(add_transaction(summary, draw_limit, start + timedelta(day), day))
#         except Exception as e:
#             #print(e)
#             continue
#
#     #print(transactions)
#
#     end_day = start + timedelta(number)
#
#     txns = '<Transactions startDate="{}" endDate="{}">'.format(start_day, str(end_day.date()))
#
#     cdata_str = c_data_str + summary_str + txns + "".join(txn for txn in transactions) + end_str
#
#     #print(cdata_str)
#
#     top = Element('UserAccountTrans')
#
#     useraccount = SubElement(top, 'UserAccount', {})
#
#     acc_ref_no = SubElement(useraccount, 'accountRefNo', {})
#     acc_ref_no.text = data_dict['accountRefNo']
#     acc_no = SubElement(useraccount, 'accountNo', {})
#     acc_no.text = data_dict['accountNo']
#     fi_type = SubElement(useraccount, 'FIType', {})
#     fi_type.text = 'DEPOSIT'
#     acc_type_enum = SubElement(useraccount, 'accountTypeEnum', {})
#     acc_type_enum.text = 'CURRENT'
#     acc_data = SubElement(useraccount, 'accountData', {})
#     acc_data.text = cdata_str
#
#     Headers = {'Content-type': 'application/xml'}
#
#     print(unescape(tostring(top).decode()))
#
#     r = requests.post(trans_api, data=unescape(tostring(top).decode()), headers=Headers)
#     print(r.text)
#
#     return 0
