package main

import (
	"bytes"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"encoding/json"
	"os"
	//"strings"

	//"strings"
)

type Configuration struct {
	ToshlToken string
}

type ToshlEntry struct {
	Amount   int `json:"amount"`
	Date     string `json:"date"`
	Account  string `json:"account"`
	Category string `json:"category"`
	Currency Currency `json:"currency"`
}

type Currency struct {
	Code string `json:"code"`
}

func main() {
	config := getConfig()

	//// Get user's details
	//selfRes := createRequest("GET", "https://api.toshl.com/me", nil, config)
	//var self map[string]interface{}
	//err := json.Unmarshal(selfRes, &self)
	//if err != nil {
	//	fmt.Println(err)
	//}
	//userId := self["id"]
	//fmt.Println(userId)

	// Get user's accounts
	accountsRes := createRequest("GET", "https://api.toshl.com/accounts", nil, config)
	var accounts []map[string]interface{}
	err := json.Unmarshal(accountsRes, &accounts)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(accounts[0]["id"])

	// Get user's categories
	categoriesRes := createRequest("GET", "https://api.toshl.com/categories", nil, config)
	var categories []map[string]interface{}
	err = json.Unmarshal(categoriesRes, &categories)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(categories[1]["id"])

	// Create entry in Toshl
	requestBody := createToshlEntryDetails("2020-10-01", 100, categories[1]["id"].(string), accounts[0]["id"].(string))
	_ = createRequest("POST", "https://api.toshl.com/entries", bytes.NewBuffer(requestBody), config)
}

func createToshlEntryDetails(date string, amount int, category string, account string) []byte {
	toshlEntry := ToshlEntry{
		Amount:   amount * -1,
		Date:     date,
		Account:  account,
		Category: category,
		Currency: Currency {
    		Code: "USD",
		},
	}

	toshlEntryBody, err := json.Marshal(toshlEntry)

	if err != nil {
		fmt.Println(err)
	}

	fmt.Println(bytes.NewBuffer(toshlEntryBody))

	return toshlEntryBody
}

func createRequest(method string, url string, requestBody io.Reader, config Configuration) []byte {
	req, err := http.NewRequest(method, url, requestBody)

	if err != nil {
		fmt.Println(err)
	}

	req = addHeaders(req, method, config)

	hc := http.Client{}
	resp, err := hc.Do(req)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(resp.StatusCode)
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(string(body))

	return body
}

func getConfig() Configuration {
	file, _ := os.Open("config.json")
	defer file.Close()
	decoder := json.NewDecoder(file)
	configuration := Configuration{}
	err := decoder.Decode(&configuration)
	if err != nil {
		fmt.Println("error getting config:", err)
	}

	return configuration
}

func addHeaders(req *http.Request, method string, config Configuration) *http.Request {
	req.Header.Add("Authorization", "Bearer " + config.ToshlToken)

	if method == "POST" {
		req.Header.Add("Content-Type", "application/json")
	}

	return req
}
