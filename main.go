package main

import (
	"fmt"
	"io"
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
	config := getConfig()

	// Get user's details
	selfRes := createRequest("GET", "https://api.toshl.com/me", nil, config)
	var self map[string]interface{}
	err := json.Unmarshal(selfRes, &self)
	if err != nil {
		fmt.Println(err)
	}
	id := self["id"]
	fmt.Println(id)

	// Get user's categories
	categoriesRes := createRequest("GET", "https://api.toshl.com/categories", nil, config)
	var categories []map[string]interface{}
	err = json.Unmarshal(categoriesRes, &categories)
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println(categories[0]["id"])

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

func createRequest(method string, url string, requestBody io.Reader, config Configuration) []byte {
	req, err := http.NewRequest(method, url, requestBody)

	if err != nil {
		fmt.Println(err)
	}

	req = addHeaders(req, config)

	hc := http.Client{}
	resp, err := hc.Do(req)
	if err != nil {
		fmt.Println(err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
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

func addHeaders(req *http.Request, config Configuration) *http.Request {
	req.Header.Add("Authorization", "Bearer " + config.ToshlToken)
	return req
}
