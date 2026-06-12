# will i be able to use functions in some areas forexample when I want to query a database
# Yes, absolutely. You can call functions anywhere inside the endpoint. For example:


# elif parts[0] == "2":
#     if len(parts) == 3:
#         amt = parts[2]
#         phone = parts[1]
#         if amt.isnumeric():
#             credit_airtime(phone, int(amt))  # call your function here
#             response = f"END {phone} has been credited with {amt} Shs."
# # For database queries, the typical pattern is:


# def get_balance(phone_number):
#     # query your database here
#     return db.query("SELECT balance FROM accounts WHERE phone = ?", phone_number)

# elif parts[0] == "1" and parts[1] == "2":
#     balance = get_balance(phoneNumber)
#     response = f"END Your account balance is {balance} Shs."