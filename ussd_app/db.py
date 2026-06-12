import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "HospitalAdmin2024!",
    "database": "ussd_db"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_or_create_account(phone_number):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM accounts WHERE phone_number = %s", (phone_number,))
    account = cursor.fetchone()
    if not account:
        cursor.execute(
            "INSERT INTO accounts (phone_number, acct_bal, airtime) VALUES (%s, %s, %s)",
            (phone_number, 1000.00, 300.00)
        )
        conn.commit()
        account = {"phone_number": phone_number, "acct_bal": 1000.00, "airtime": 300.00}
    cursor.close()
    conn.close()
    return account

def get_balance(phone_number):
    account = get_or_create_account(phone_number)
    return account["acct_bal"]

def get_airtime(phone_number):
    account = get_or_create_account(phone_number)
    return account["airtime"]

def deduct_balance(phone_number, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE accounts SET acct_bal = acct_bal - %s WHERE phone_number = %s",
        (amount, phone_number)
    )
    conn.commit()
    cursor.close()
    conn.close()

def reset_balance(phone_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE accounts SET acct_bal = 1000.00 WHERE phone_number = %s",
        (phone_number,)
    )
    conn.commit()
    cursor.close()
    conn.close()
