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
	fmt.Println("Splitwise to Toshl expense transfer tool")
	fmt.Println("")
	fmt.Print("Loading config... ")
	config := getConfig()
	if config == nil {
		return
	}
	fmt.Println("done")

	var authSuccess bool = true
	// Get Splitwise user
	fmt.Print("Checking splitwise token... ")
	// datedBefore := "2020-11-01"
	// datedAfter := "2020-10-01"
	// splitwiseURL := "https://secure.splitwise.com/api/v3.0/get_expenses?dated_before=" + datedBefore + "&dated_after=" + datedAfter
	splitwiseURL := "https://secure.splitwise.com/api/v3.0/get_current_user"
	swRes := createdSplitwiseRequest("GET", splitwiseURL, nil, config)
	var swUser map[string]interface{}
	err := json.Unmarshal(swRes, &swUser)
	fmt.Println(swUser["user"]["email"])

	swError, swHasError := swUser["error"]
	if err != nil || swHasError {
		fmt.Println("error")
		fmt.Println(swError)
		authSuccess = false
	} else {
		fmt.Print(swUser["error"])
		fmt.Println("done")
	}

	// Get Toshl user
	fmt.Print("Checking toshl token... ")
	tRes := createToshlRequest("GET", "https://api.toshl.com/me", nil, config)
	var tUser map[string]interface{}
	err = json.Unmarshal(tRes, &tUser)
	fmt.Println(tUser)
	fmt.Println(err)
	tError, tHasError := tUser["error_id"]
	if err != nil || tHasError {
		fmt.Println("error")
		fmt.Println(tError)
		authSuccess = false
	} else {
		fmt.Println("done")
	}

	if !authSuccess {
		fmt.Println("There are errors with one or both of your authorisation tokens. Please check to make sure the tokens are correct and run this script again.")
		return
	}

	fmt.Println("Successfully authenticated with both services.")

	fmt.Println("What would you like to do now?")
	fmt.Println("1. Load splitwise users")

	// fmt.Println(accounts[0]["id"])

	// // Get Toshl user's categories
	// categoriesRes := createToshlRequest("GET", "https://api.toshl.com/categories", nil, config)
	// var categories []map[string]interface{}
	// err = json.Unmarshal(categoriesRes, &categories)
	// if err != nil {
	// 	fmt.Println(err)
	// }
	// fmt.Println(categories[1]["id"])

	// // Create entry in Toshl
	// requestBody := createToshlEntryDetails("2020-10-01", 100, categories[1]["id"].(string), accounts[0]["id"].(string))
	// _ = createToshlRequest("POST", "https://api.toshl.com/entries", bytes.NewBuffer(requestBody), config)
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

func createToshlRequest(method string, url string, requestBody io.Reader, config *Configuration) []byte {
	return createRequest(method, url, requestBody, config.ToshlToken)
}

func createdSplitwiseRequest(method string, url string, requestBody io.Reader, config *Configuration) []byte {
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
	// fmt.Println(string(body))

	return body
}

// Get the configuration
func getConfig() *Configuration {
	if _, err := os.Stat("config.json"); os.IsNotExist(err) {
		// config does not exist
		fmt.Println("error:\nConfig file does not exist.\nPlease create a config.json file using config.example.json as an example.")
		return nil
	}
	file, _ := os.Open("config.json")
	defer file.Close()
	decoder := json.NewDecoder(file)
	configuration := Configuration{}
	err := decoder.Decode(&configuration)
	if err != nil {
		fmt.Println("error: Cannot decode config\n", err)
		return nil
	}

	return &configuration
}

func addHeaders(req *http.Request, method string, token string) *http.Request {
	req.Header.Add("Authorization", "Bearer "+token)

	if method == "POST" {
		req.Header.Add("Content-Type", "application/json")
	}

	return req
}
