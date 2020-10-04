package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"encoding/json"
	"os"
	//"strings"
)

type Configuration struct {
	ToshlToken string
}

func main() {
	file, _ := os.Open("config.json")
	defer file.Close()
	decoder := json.NewDecoder(file)
	configuration := Configuration{}
	err := decoder.Decode(&configuration)
	if err != nil {
		fmt.Println("error getting config:", err)
	}

	// Get user details
	req, err := http.NewRequest("GET", "https://api.toshl.com/me", nil)

	if err != nil {
		fmt.Println(err)
	}

	req.Header.Add("Authorization", "Bearer " + configuration.ToshlToken)

	hc := http.Client{}
	resp, err := hc.Do(req)
	if err != nil {
		fmt.Println(err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	fmt.Println(string(body))

	//requestBody := strings.NewReader(`
	//	{
	//		"amount": "100",
	//		"currency": {
	//			"code": "USD"
	//		},
	//		"date": "2020-10-01",
	//		"account": "123",
	//		"category": "123"
	//	}
	//`)
	//
	//req, err := http.NewRequest("POST", "https://api.toshl.com/entries", requestBody)
	//
	//hc := http.Client{}
	//resp, err := hc.Do(req)
}
