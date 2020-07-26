import requests
import  json
import jwt
from AABharatFed import settings
import datetime
import uuid
def makeDetatchedJWS(payload):
    f = open("private.pem", "r")
    key=f.read()
    print(key)
    try:
        encoded = jwt.encode(payload, key, algorithm='RS256').decode('UTF-8')
        splittedJWS = encoded.split(".")
        splittedJWS[1] = ""
        return '.'.join(splittedJWS)
    except Exception as ex:
        print(ex)


def consent_req():
    url='https://aauat.finvu.in/API/V1/Consent'
    payload={
        "ver": "1.1.3",
        "timestamp": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "txnid": str(uuid.uuid4()),
        "ConsentDetail": {
          "consentStart": "2020-7-23T11:39:57.153Z",
          "consentExpiry": "2020-12-06T11:39:57.153Z",
          "consentMode": "VIEW",
          "fetchType": "PERIODIC",
          "consentTypes": [
            "TRANSACTIONS"
          ],
          "fiTypes": [
            "DEPOSIT"
          ],

          "Customer": {
            "id": "9910423393@finvu"
          },
          "Purpose": {
            "code": "101",
            "refUri": "https://api.rebit.org.in/aa/purpose/101.xml",
            "text": "BharatApp",
            "Category": {
        "type": "string"
            }
          },
          "FIDataRange": {
            "from": "2018-10-31T04:10:12.898",
        "to": "2020-5-31T04:10:12.897"
          },
          "DataLife": {
            "unit": "YEAR",
            "value": 1
          },
          "Frequency": {
            "unit": "MONTH",
            "value": 1
          }

        }
      }
    make_toke_req(url,payload)




def make_toke_req(url,payload):
    api_key='eyJraWQiOiJhYWthc2h0ZXdhcmlAZ21haWwuY29tIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJjb29raWVqYXIiLCJleHAiOjE2MjcwMjAyMzQsImp0aSI6IjN0bHBvV0pJNDFrY053Uk1TdE8tNVEiLCJpYXQiOjE1OTU0ODQyMzcsIm5iZiI6MTU5NTQ4NDIzNywic3ViIjoiYWFrYXNodGV3YXJpQGdtYWlsLmNvbSIsImdyb3VwcyI6WyJhZ2dyZWdhdG9yIl19.amdrVOZnZV_9RVs0dVtGxmtju0lBQ3X5v4Osani5Gkz7Sh5AcFpKhgGUAp7PfIEhFZIIy4wdN9KIWtO5Y21SHuQYp8Vnv2x7L1ZHEDaQIiSL-D2OWGeWRk2Z6wxXG2httI6TKgaO3J4ZZGuGCrw-JORv6yhe5HzNVAi9NZFOx6zZ5qXAEVbEKdRpN4pA_VoOjwBfOSa65cYTSQL_GPx0qgNfT8BVqp8naX1xUPBftpa7r7lAGiSvZAfWt5dcLyoJzjCh42bVqfSRh671BPUIxjoEmcLs29HNUM6q8bS0h_EvxT1moljRSsc_h0PpgMvArcnzMhXOsnSg0u_KSTd2fw'
    jws=makeDetatchedJWS(payload)
    headers={
'fip_api_key':api_key,
        'x-jws-signature':jws
    }
    return requests.post(url,json=payload,proxies=settings.proxy,verify=False,headers=headers)