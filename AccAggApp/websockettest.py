# wss://wssdev.finvu.in/api
greeting = '{"header":{"mid":"s-f7a3-4269-9a02-e9c8552aee45","ts":"2020-07-16T20:02:58.550Z","sid":null,"dup":false,"type":"urn:finvu:in:app:req.register.01"},"payload":{"mobileno":"9910423393","username":"aakashqq@finvu","password":"2468","repassword":"2468"}}'
greeting = '{"header": {"mid": "efb89059-c7af-11ea-90da-94e6f7a3cb84", "ts": "2020-07-17T03:31:46.258Z", "sid": "null", "dup": "false", "type": "urn:finvu:in:app:req.register.01"}, "payload": {"mobileno": "9910423393", "username": "aki3322@finvu", "password": "2468", "repassword": "2468"}}'
greeting = '{"header":{"mid":"6740da48-1936-4fc2-9525-c2d8a1d3d923","ts":"2020-07-16T22:14:36.798Z","sid":null,"dup":false,"type":"urn:finvu:in:app:req.register.01"},"payload":{"mobileno":"9910423369","username":"aaadd3f`@finvu","password":"2468","repassword":"2468"}}'
greeting = '{"header":{"mid":"61696c41-b267-4c1f-a0c5-2551ee0c6df4","ts":"2020-07-16T22:20:34.957Z","sid":null,"dup":false,"type":"urn:finvu:in:app:req.register.01"},"payload":{"mobileno":"9910423369","username":"aaaddd3f`@finvu","password":"2468","repassword":"2468"}}'
greeting = '{"header": {"mid": "8a6f6bca-8a0f-44b4-ae06-b3a5a4d9660b", "ts": "2020-07-16T22:22:51.012Z", "sid": "null", "dup": "false", "type": "urn:finvu:in:app:req.register.01"}, "payload": {"mobileno": "9910423393", "username": "d3333@finvu", "password": "2468", "repassword": "2468"}}'
wgreet = '{"header":{"mid":"079f8dbf-063f-40e4-b580-7b544c9f27d4","ts":"2020-07-16T22:14:36.798Z","sid":null,"dup":false,"type":"urn:finvu:in:app:req.register.01"},"payload":{"mobileno":"9910423369","username":"aaadd3`@finvu","password":"2468","repassword":"2468"}}'
notw = '{"header":{"mid":"s-f7a3-4269-9a02-e9c8552aee45","ts":"2020-07-16T22:34:41.476Z","sid":null,"dup":false,"type":"urn:finvu:in:app:req.register.01"},"payload":{"mobileno":"9988998899","username":"aas1244F2@finvu","password":"2468","repassword":"2468"}}'
# {"header": {"mid": "efb89059-c7af-11ea-90da-94e6f7a3cb80", "ts": "2020-07-17T03:31:46.258859Z", "sid": "null", "dup": "false", "type": "urn:finvu:in:app:req.register.01"}, "payload": {"mobileno": "9910423393", "username": "aki3322@finvu", "password": "2468", "repassword": "2468"}}


# import asyncio
# import websockets
#
# async def hello():
#     uri = "wss://wssdev.finvu.in/api"
#     async with websockets.connect(uri) as websocket:
#
#         greeting = '{"header":{"mid":"c36f3381-f7a3-4269-9a01-e9c8552aee45","ts":"2020-07-16T20:02:58.550Z","sid":null,"dup":false,"type":"urn:finvu:in:app:req.register.01"},"payload":{"mobileno":"9910423393","username":"aakashqq@finvu","password":"2468","repassword":"2468"}}'
#
#         await websocket.send(greeting)
#         print(f"> {greeting}")
#
#         greeting = await websocket.recv()
#         print(f"< {greeting}")
#
# asyncio.get_event_loop().run_until_complete(hello())

import websocket

ws = websocket.WebSocket()
ws.connect("wss://wssdev.finvu.in/api")

print(notw)

ws.send(notw)

result = ws.recv()
print(result)
