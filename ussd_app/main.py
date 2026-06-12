from fastapi import FastAPI, Request
app = FastAPI()


import requests
import os

SANDBOX_API_KEY = "atsk_93ff51f0ae230666ec14c8e0f0bafeb6d51e51cf852b4bf3d5abf0e575cc9a8399b3bf59"

SANDBOX_URL = "https://api.sandbox.africastalking.com/version1/messaging"

USSD_CODE = "13441"

@app.get('/')
async def root():
    return {'message': 'Hello world to you'}



@app.post("/sms_callback")
async def sms_callback(request: Request):
    body = await request.body()
    form = await request.form()
    wording = dict(form)
    print("Raw body:", body)
    print("Form data:", dict(form))
    response_to_sms(wording['from'], "Thank you sender for this message")

    return {"status": "success"}


# url -X POST \
#     https://api.africastalking.com/version1/messaging/bulk \
#     -H 'Accept: application/json' \
#     -H 'Content-Type: application/json' \
#     -H 'apiKey: MyAppApiKey' \
#     -d '{
#     "username": "username",
#     "message": "This is a sample message.",
#     "senderId": "ABC",
#     "phoneNumbers": [
#         "+254711XXXYYY",
#         "+254711YYYZZZ"
#     ]
# }'

def response_to_sms(phone_number, message):
    response = requests.post(SANDBOX_URL, data =
                  {"username": "sandbox",
                   "to": phone_number,
                   "message": message,
                   "from": USSD_CODE},

                  headers= {"apiKey": SANDBOX_API_KEY,
                            "Accept": "application/json",
                            "Content-Type": "application/x-www-form-urlencoded"}
                            )
    print("AT response:", response.status_code, response.text)
    



