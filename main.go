package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
)

// Configuration provides the application configuration data
type Configuration struct {
	ToshlToken     string
	SplitwiseToken string
}

// ToshlEntry is the format that the Toshl API requires for an entry.
type ToshlEntry struct {
	Amount   int      `json:"amount"`
	Date     string   `json:"date"`
	Account  string   `json:"account"`
	Category string   `json:"category"`
	Currency Currency `json:"currency"`
}

// Currency is part of ToshlEntry
type Currency struct {
	Code string `json:"code"`
}

func main() {
	config := getConfig()

	// Get Splitwise expenses
	datedBefore := "2020-11-01"
	datedAfter := "2020-10-01"
	splitwiseURL := "https://secure.splitwise.com/api/v3.0/get_expenses?dated_before=" + datedBefore + "&dated_after=" + datedAfter
	userRes := createdSplitwiseRequest("GET", splitwiseURL, nil, config)
	var user map[string]interface{}
	err := json.Unmarshal(userRes, &user)
	if err != nil {
		fmt.Println(err)
	}

	// Get Toshl user's accounts
	accountsRes := createToshlRequest("GET", "https://api.toshl.com/accounts", nil, config)
	var accounts []map[string]interface{}
	err = json.Unmarshal(accountsRes, &accounts)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(accounts[0]["id"])

	// Get Toshl user's categories
	categoriesRes := createToshlRequest("GET", "https://api.toshl.com/categories", nil, config)
	var categories []map[string]interface{}
	err = json.Unmarshal(categoriesRes, &categories)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(categories[1]["id"])

	// Create entry in Toshl
	requestBody := createToshlEntryDetails("2020-10-01", 100, categories[1]["id"].(string), accounts[0]["id"].(string))
	_ = createToshlRequest("POST", "https://api.toshl.com/entries", bytes.NewBuffer(requestBody), config)
}

func createToshlEntryDetails(date string, amount int, category string, account string) []byte {
	toshlEntry := ToshlEntry{
		Amount:   amount * -1,
		Date:     date,
		Account:  account,
		Category: category,
		Currency: Currency{
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

func createToshlRequest(method string, url string, requestBody io.Reader, config Configuration) []byte {
	return createRequest(method, url, requestBody, config.ToshlToken)
}

func createdSplitwiseRequest(method string, url string, requestBody io.Reader, config Configuration) []byte {
	return createRequest(method, url, requestBody, config.SplitwiseToken)
}

func createRequest(method string, url string, requestBody io.Reader, apiKey string) []byte {
	req, err := http.NewRequest(method, url, requestBody)

	if err != nil {
		fmt.Println(err)
	}

	req = addHeaders(req, method, apiKey)

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

func addHeaders(req *http.Request, method string, token string) *http.Request {
	req.Header.Add("Authorization", "Bearer "+token)

	if method == "POST" {
		req.Header.Add("Content-Type", "application/json")
	}

	return req
}
