package test

import (
    "testing"
    "net/http"
    "encoding/json"
    "bytes"
    "strconv"

    "authorization_service/internal/service"
)

func TestEmptyProducts(t *testing.T) {
    clearTable()

    req, _ := http.NewRequest("GET", "/products", nil)
    response := executeRequest(req)

    checkResponseCode(t, http.StatusOK, response.Code)

    if body := response.Body.String(); body != "[]" {
        t.Errorf("Expected an empty array. Got %s", body)
    }
}

func TestGetNonExistentProduct(t *testing.T) {
    clearTable()

    req, _ := http.NewRequest("GET", "/products/11", nil)
    response := executeRequest(req)

    checkResponseCode(t, http.StatusNotFound, response.Code)

    var m map[string]string
    json.Unmarshal(response.Body.Bytes(), &m)
    if m["error"] != "Product not found" {
        t.Errorf("Expected the 'error' key of the response to be set to 'Product not found'. Got '%s'", m["error"])
    }
}

func TestCreateProduct(t *testing.T) {
    clearTable()

    payload := []byte(`{"name":"test_product","metadata":"{\"blah\":\"123\"}"}`)

    req, _ := http.NewRequest("POST", "/products", bytes.NewBuffer(payload))
    response := executeRequest(req)

    checkResponseCode(t, http.StatusCreated, response.Code)

    var m service.Product
    json.Unmarshal(response.Body.Bytes(), &m)

    if m.Name != "test_product" {
        t.Errorf("Expected product name to be 'test_product'. Got '%v'", m.Name)
    }

    expected_metadata := "{\"blah\":\"123\"}"
    if m.Metadata != expected_metadata {
        t.Errorf("Expected product metadata to be '%s'. Got '%v'", expected_metadata, m.Metadata)
    }

    if m.ID != 1 {
        t.Errorf("Expected product ID to be '1'. Got '%v'", m.ID)
    }
}

func TestGetProduct(t *testing.T) {
    clearTable()
    addProducts(1)

    req, _ := http.NewRequest("GET", "/products/1", nil)
    response := executeRequest(req)

    checkResponseCode(t, http.StatusOK, response.Code)
}

func TestUpdateProduct(t *testing.T) {
    clearTable()
    addProducts(1)

    req, _ := http.NewRequest("GET", "/products/1", nil)
    response := executeRequest(req)
    var originalProduct service.Product
    json.Unmarshal(response.Body.Bytes(), &originalProduct)

    payload := []byte(`{"name":"test product - updated name","metadata":"{\"bleh\":\"456\"}"}`)

    req, _ = http.NewRequest("PUT", "/products/1", bytes.NewBuffer(payload))
    response = executeRequest(req)

    checkResponseCode(t, http.StatusOK, response.Code)

    var m service.Product
    json.Unmarshal(response.Body.Bytes(), &m)

    if m.ID != originalProduct.ID {
        t.Errorf("Expected the id to remain the same (%v). Got %v", originalProduct.ID, m.ID)
    }

    if m.Name == originalProduct.Name {
        t.Errorf("Expected the name to change from '%v' to '%v'. Got '%v'", originalProduct.Name, m.Name, m.Name)
    }

    if m.Metadata == originalProduct.Metadata {
        t.Errorf("Expected the metadata to change from '%v' to '%v'. Got '%v'", originalProduct.Metadata, m.Metadata, m.Metadata)
    }
}

func TestDeleteProduct(t *testing.T) {
    clearTable()
    addProducts(1)

    req, _ := http.NewRequest("GET", "/products/1", nil)
    response := executeRequest(req)
    checkResponseCode(t, http.StatusOK, response.Code)

    req, _ = http.NewRequest("DELETE", "/products/1", nil)
    response = executeRequest(req)

    checkResponseCode(t, http.StatusOK, response.Code)

    req, _ = http.NewRequest("GET", "/products/1", nil)
    response = executeRequest(req)
    checkResponseCode(t, http.StatusNotFound, response.Code)
}

func TestGetProducts(t *testing.T) {
    clearTable()
    addProducts(1)
    addProducts(2)

    req, _ := http.NewRequest("GET", "/products", nil)
    response := executeRequest(req)

    checkResponseCode(t, http.StatusOK, response.Code)

    var m []service.Product
    json.Unmarshal(response.Body.Bytes(), &m)

    if len(m) != 2 {
        t.Errorf("Expected length 2. Got '%v'", len(m))
    }

    result := m[0].Name
    expected := "Product0"
    if result != expected {
        t.Errorf("Expected product name to be '%v'. Got '%v'", expected, result)
    }

    result = m[1].Name
    expected = "Product1"
    if result != expected {
        t.Errorf("Expected product name to be '%v'. Got '%v'", expected, result)
    }
}

func TestGetProductsWithFilter(t *testing.T) {
    clearTable()
    addProducts(1)
    addProducts(2)

    req, _ := http.NewRequest("GET", "/products?name=Product1", nil)
    response := executeRequest(req)

    checkResponseCode(t, http.StatusOK, response.Code)

    var m []service.Product
    json.Unmarshal(response.Body.Bytes(), &m)

    if len(m) != 1 {
        t.Errorf("Expected length 1. Got '%v'", len(m))
    }

    result := m[0].Name
    expected := "Product1"
    if result != expected {
        t.Errorf("Expected product name to be '%v'. Got '%v'", expected, result)
    }
}

// Helpers

func addProducts(count int) {
    if count < 1 {
        count = 1
    }

    for i := 0; i < count; i++ {
        a.DB.Exec("INSERT INTO auth.products(name, metadata) VALUES($1, $2)", "Product"+strconv.Itoa(i), (i+1.0)*10)
    }
}
