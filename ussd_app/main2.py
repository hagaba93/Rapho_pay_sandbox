from fastapi import FastAPI, Form, Response
from db import get_balance, get_airtime, deduct_balance, reset_balance

app = FastAPI()

@app.post("/ussd_callback")
async def ussd_callback(
    sessionId: str = Form(...),
    serviceCode: str = Form(...),
    phoneNumber: str = Form(...),
    text: str = Form("")
):
    parts = text.split("*") if text else []

    if text == "":
        response = ("CON Welcome to Rapho Pay\n"
                    "1. Check Balance\n"
                    "2. Buy Airtime\n"
                    "3. Fund Transfer")

    elif parts[0] == "1":
        if len(parts) == 1:
            response = ("CON Select what you are looking for?\n"
                        "1. Airtime\n"
                        "2. Account balance\n"
                        "3. Reset balance")
        elif parts[1] == "1":
            airtime = get_airtime(phoneNumber)
            response = f"END Your airtime balance is {airtime} Shs."
        elif parts[1] == "2":
            balance = get_balance(phoneNumber)
            response = f"END Your account balance is {balance} Shs."
        elif parts[1] == "3":
            reset_balance(phoneNumber)
            response = "END Your balance has been reset to 1000 Shs."
        else:
            response = "END Invalid input"

    elif parts[0] == "2":
        if len(parts) == 1:
            response = "CON Enter phone number to load airtime:"
        elif len(parts) == 2:
            phone = parts[1]
            if len(phone) == 11 and phone.isnumeric():
                response = "CON Enter the amount to load:"
            else:
                response = "END Invalid phone number. Must be 11 digits."
        elif len(parts) == 3:
            amt = parts[2]
            if amt.isnumeric():
                response = f"END The number {parts[1]} has been credited with {amt} Shs."
            else:
                response = "END Invalid amount"

    elif parts[0] == "3":
        if len(parts) == 1:
            response = "CON Enter phone number to transfer to:"
        elif len(parts) == 2:
            phone = parts[1]
            if len(phone) == 11 and phone.isnumeric():
                response = "CON Enter the amount to transfer:"
            else:
                response = "END Invalid phone number. Must be 11 digits."
        elif len(parts) == 3:
            fund = parts[2]
            balance = get_balance(phoneNumber)
            if fund.isnumeric() and int(fund) > 0 and int(fund) <= balance:
                deduct_balance(phoneNumber, int(fund))
                new_balance = get_balance(phoneNumber)
                response = (f"END {fund} Shs has been transferred to {parts[1]}\n"
                            f"Your account balance is {new_balance} Shs.")
            elif fund.isnumeric() and int(fund) > balance:
                response = "END Insufficient balance."
            else:
                response = "END Invalid amount"

    else:
        response = "END Invalid input"

    return Response(content=response, media_type="text/plain")
