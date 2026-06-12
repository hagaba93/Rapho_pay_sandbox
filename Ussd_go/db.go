package main

import (
    "database/sql"
    "log"
    "strconv"
    "unicode"

    _ "github.com/go-sql-driver/mysql"
)

var db *sql.DB

func init() {
    var err error
    db, err = sql.Open("mysql", "root:HospitalAdmin2024!@tcp(localhost:3306)/ussd_db")
    if err != nil {
        log.Fatal(err)
    }
}

func getOrCreateAccount(phoneNumber string) (float64, float64) {
    var acctBal, airtime float64
    err := db.QueryRow("SELECT acct_bal, airtime FROM accounts WHERE phone_number = ?", phoneNumber).Scan(&acctBal, &airtime)
    if err == sql.ErrNoRows {
        db.Exec("INSERT INTO accounts (phone_number, acct_bal, airtime) VALUES (?, ?, ?)", phoneNumber, 1000.00, 300.00)
        return 1000.00, 300.00
    }
    return acctBal, airtime
}

func getBalance(phoneNumber string) float64  { bal, _ := getOrCreateAccount(phoneNumber); return bal }
func getAirtime(phoneNumber string) float64  { _, air := getOrCreateAccount(phoneNumber); return air }

func deductBalance(phoneNumber string, amount int) {
    db.Exec("UPDATE accounts SET acct_bal = acct_bal - ? WHERE phone_number = ?", amount, phoneNumber)
}

func resetBalance(phoneNumber string) {
    db.Exec("UPDATE accounts SET acct_bal = 1000.00 WHERE phone_number = ?", phoneNumber)
}

func isNumeric(s string) bool {
    if len(s) == 0 { return false }
    for _, c := range s { if !unicode.IsDigit(c) { return false } }
    return true
}

func toInt(s string) int { n, _ := strconv.Atoi(s); return n }
