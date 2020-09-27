package main

import (
	"net/http"
	"strings"
)

func main() {
	requestBody := strings.NewReader(`
		{
			"amount": "100",
			"currency": {
				"code": "USD"
			},
			"date": "2020-10-01",
			"account": "123",
			"category": "123"
		}
	`)

	req, err := http.NewRequest("POST", "https://api.toshl.com/entries", requestBody)

	if err != nil {
		req.Header.Add("Content-Type", "application/json")
		req.Header.Add("Authorization", "Bearer 123")
	}

	hc := http.Client{}
	resp, err := hc.Do(req)
}
