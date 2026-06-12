acct_bal = 1000
airtime = 300
def checkbalance():
    bal_code = input("Select what you are looking for?\n"
                     "1. Airtime\n"
                     "2. Account balance\n"
                     "#. back to main menu\n"
                     "0. exit"
                     )
    if bal_code == "1":
        print(f"Your airtime balance is {airtime} Shs.")
    elif bal_code == "2":
        print(f"Your account balance is {acct_bal} Shs.")
    
    else:
        print("Invalid input\n"
              "Enter # to go back to the main menu or press 0 to exit")
        checkbalance()

def checkamount(sim):
    amt = input("Enter the amount to load: ")
    if amt.isnumeric():
        print(f"The number {sim} has been credited with {amt} Shs.")
    
    elif amt == "#":
        TransEntry()
    else:
        print("Invalid input\n"
              "try again or press # to return to main menu")
        checkamount(sim)

def transfer_fund(phone):
    global acct_bal
    fund = input("Enter the amount to transfer: ")
    if fund.isnumeric() and int(fund) <= acct_bal and int(fund) > 0:
        acct_bal -= int(fund)
        print(f"{fund} Shs has been transfered to {phone}\n"
              f"Your account balance is {acct_bal} Shs.")
    elif fund == "0":
        print(f"Please input an amount greater than 0")
        transfer_fund(phone)
    elif fund == "#":
        TransEntry()
    else:
        print("Invalid input\n"
              "try again or press # to return to main menu")
        transfer_fund(phone)




def AirtimeTrans():
    phone = input("Enter phone number to load airtime: ")
    if len(phone) == 11 and phone.isnumeric():
        checkamount(phone)
    elif phone == "#":
        TransEntry()
    else:
        print("invalid input.\n"
              "Try again or press # to return to the main menu")
        AirtimeTrans()
        
def fundTransfer():
    # fund = input("Enter amount to transfer") 
    phone = input("Enter phone number to load airtime: ")
    if len(phone) == 11 and phone.isnumeric():
        transfer_fund(phone)
    else:
        print("invalid input.\n"
              "Try again or press # to return to the main menu")
        fundTransfer()




def ConfirmUssd():
    Ussd = input("Enter ussd code: ")
    if Ussd == "*123#":
        print("Welcome to Rapho Pay")
        TransEntry()

    elif Ussd == "0":
        print("app exited")
    else:
        print("Invalid ussd code\n"
              "Try again with right code\n"
              "or press 0 to exit")
        ConfirmUssd()

def TransEntry():
    transcode = input("Select transaction\n"
                      "1. Check Balamce\n"
                      "2. Buy Airtime\n"
                    "3. Fund transfer\n" )
    if transcode == "1":
        checkbalance()
    elif transcode == "2":
        AirtimeTrans()

    elif transcode == "3":
        fundTransfer()
    



        
ConfirmUssd()

# running the fast api code
# uvicorn main2:app --reload 
# python main2.py
    