package main

import (
    "fmt"
    "net/http"
    "strings"
)

func main() {
    http.HandleFunc("/ussd_callback", ussdCallback)
    fmt.Println("Server running on :8000")
    http.ListenAndServe(":8000", nil)
}

func ussdCallback(w http.ResponseWriter, r *http.Request) {
    r.ParseForm()
    phoneNumber := r.FormValue("phoneNumber")
    text := r.FormValue("text")

    var parts []string
    if text != "" {
        parts = strings.Split(text, "*")
    }

    var response string

    switch {
    case text == "":
        response = "CON Welcome to Rapho Pay\n1. Check Balance\n2. Buy Airtime\n3. Fund Transfer"

    case parts[0] == "1":
        switch {
        case len(parts) == 1:
            response = "CON Select what you are looking for?\n1. Airtime\n2. Account balance\n3. Reset balance"
        case parts[1] == "1":
            response = fmt.Sprintf("END Your airtime balance is %.2f Shs.", getAirtime(phoneNumber))
        case parts[1] == "2":
            response = fmt.Sprintf("END Your account balance is %.2f Shs.", getBalance(phoneNumber))
        case parts[1] == "3":
            resetBalance(phoneNumber)
            response = "END Your balance has been reset to 1000 Shs."
        default:
            response = "END Invalid input"
        }

    case parts[0] == "2":
        switch {
        case len(parts) == 1:
            response = "CON Enter phone number to load airtime:"
        case len(parts) == 2:
            if len(parts[1]) == 11 && isNumeric(parts[1]) {
                response = "CON Enter the amount to load:"
            } else {
                response = "END Invalid phone number. Must be 11 digits."
            }
        case len(parts) == 3:
            if isNumeric(parts[2]) {
                response = fmt.Sprintf("END The number %s has been credited with %s Shs.", parts[1], parts[2])
            } else {
                response = "END Invalid amount"
            }
        }

    case parts[0] == "3":
        switch {
        case len(parts) == 1:
            response = "CON Enter phone number to transfer to:"
        case len(parts) == 2:
            if len(parts[1]) == 11 && isNumeric(parts[1]) {
                response = "CON Enter the amount to transfer:"
            } else {
                response = "END Invalid phone number. Must be 11 digits."
            }
        case len(parts) == 3:
            fund := toInt(parts[2])
            balance := getBalance(phoneNumber)
            switch {
            case isNumeric(parts[2]) && fund > 0 && float64(fund) <= balance:
                deductBalance(phoneNumber, fund)
                response = fmt.Sprintf("END %s Shs transferred to %s\nYour balance is %.2f Shs.", parts[2], parts[1], getBalance(phoneNumber))
            case isNumeric(parts[2]) && float64(fund) > balance:
                response = "END Insufficient balance."
            default:
                response = "END Invalid amount"
            }
        }

    default:
        response = "END Invalid input"
    }

    w.Header().Set("Content-Type", "text/plain")
    fmt.Fprint(w, response)
}
