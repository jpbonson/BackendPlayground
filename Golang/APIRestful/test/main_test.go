package test

import (
    "os"
    "testing"
    "log"
    "net/http"
    "net/http/httptest"
    "authorization_service/cmd/server/router"
)

var a router.App

func TestMain(m *testing.M) {
    os.Setenv("AUTH_SERVICE_ENV", "test")

    a = router.App{}
    a.Initialize()

    ensureTableExists()

    code := m.Run()

    clearTable()

    os.Exit(code)
}

func ensureTableExists() {
    if _, err := a.DB.Exec(tableCreationQuery); err != nil {
        log.Fatal(err)
    }
}

func clearTable() {
    a.DB.Exec("DELETE FROM auth.PRODUCTS")
    a.DB.Exec("ALTER SEQUENCE auth.products_id_seq RESTART WITH 1")
}

func executeRequest(req *http.Request) *httptest.ResponseRecorder {
    rr := httptest.NewRecorder()
    a.Router.ServeHTTP(rr, req)
    return rr
}

func checkResponseCode(t *testing.T, expected, actual int) {
    if expected != actual {
        t.Errorf("Expected response code %d. Got %d\n", expected, actual)
    }
}

const tableCreationQuery = `CREATE TABLE IF NOT EXISTS auth.PRODUCTS
(
  id SERIAL PRIMARY KEY,
  name VARCHAR (50) UNIQUE NOT NULL,
  metadata TEXT
)`
