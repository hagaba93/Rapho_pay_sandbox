# pip install fastapi uvicorn requests python-multipart 

# uvicorn main:app --reload

from fastapi import FastAPI, Form
import requests
import os

app = FastAPI()

SANDBOX_API_KEY = os.getenv("SANDBOX_API_KEY", "YOUR_API_KEY_HERE")
AFRICASTALKING_USERNAME = "sandbox"
AFRICASTALKING_SENDER_ID = "8023"


@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}


@app.post("/sms_callback")
def sms_callback(
    sender: str = Form(..., alias="from"),
    text: str = Form(...)
):
    print("Sender:", sender)
    print("Message:", text)

    response_to_sms(sender, text)

    return {"status": "success"}


def response_to_sms(recipient_phone_number: str, message: str):
    response = requests.post(
        "https://api.sandbox.africastalking.com/version1/messaging",
        data={
            "username": AFRICASTALKING_USERNAME,
            "to": recipient_phone_number,
            "message": message,
            "from": AFRICASTALKING_SENDER_ID,
        },
        headers={
            "apiKey": SANDBOX_API_KEY,
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    return response.json()