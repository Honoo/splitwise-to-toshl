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
	self := createRequest("GET", "https://api.toshl.com/me", nil, config)
	id := self["id"]
	fmt.Println(id)

	// Get user's categories
	_ = createRequest("GET", "https://api.toshl.com/categories", nil, config)

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

func createRequest(method string, url string, requestBody io.Reader, config Configuration) map[string]interface{} {
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

	var bodyMap map[string]interface{}
	err = json.Unmarshal(body, &bodyMap)

	return bodyMap
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
