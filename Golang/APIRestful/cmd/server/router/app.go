package router

import (
    "database/sql"
    "fmt"
    "net/http"
    "os"

    "github.com/gorilla/mux"
    "github.com/gorilla/handlers"
    _ "github.com/lib/pq"
    log "github.com/sirupsen/logrus"
)

type Config struct {
    EnvType string
    DBName string
    Host string
    Port string
}

type App struct {
    Router *mux.Router
    DB     *sql.DB
    LogFile *os.File
    Config Config
}

func (a *App) Initialize() {
    a.setupEnvironment()
    a.setupLogger()
    a.setupDatabase()
    a.setupRoutes()
}

func (a *App) setupEnvironment() {
    config := Config{}
    config.EnvType = os.Getenv("AUTH_SERVICE_ENV")

    switch config.EnvType {
    case "test":
        config.DBName = "authorization_service_test"
        config.Host = "localhost:5432"
        config.Port = ":8000"
    case "production":
        config.DBName = "authorization_service_production"
        config.Host = "localhost:5432"
        config.Port = ":8000"
    default:
        config.EnvType = "development"
        config.DBName = "authorization_service_development"
        config.Host = "localhost:5432"
        config.Port = ":8000"
    }

    a.Config = config
}

func (a *App) setupLogger() {
    var f *os.File
    var err error
    if a.Config.EnvType == "test" {
        f = os.Stdout
    } else {
        f, err = os.OpenFile(a.Config.EnvType+".log", os.O_CREATE | os.O_WRONLY | os.O_APPEND, 0666)
        if err != nil {
            log.Panic("Access log: ", err)
        }
    }

    log.SetOutput(f)
    log.SetFormatter(&log.JSONFormatter{})
    a.LogFile = f
}

func (a *App) setupDatabase() {
    host := a.Config.Host
    dbname := a.Config.DBName
    connectionString := fmt.Sprintf("postgresql://%s/%s?sslmode=disable", host, dbname)
    var err error
    a.DB, err = sql.Open("postgres", connectionString)
    if err != nil {
        log.Fatal(err)
    }
}

func (a *App) setupRoutes() {
    a.Router = mux.NewRouter()

    // swagger:route GET /pets pets users listPets
    //
    // Lists pets filtered by some parameters.
    //
    // This will show all available pets by default.
    // You can get the pets that are out of stock
    //
    //     Consumes:
    //     - application/json
    //     - application/x-protobuf
    //
    //     Produces:
    //     - application/json
    //     - application/x-protobuf
    //
    //     Schemes: http, https, ws, wss
    //
    //     Security:
    //       api_key:
    //       oauth: read, write
    //
    //     Responses:
    //       default: genericError
    //       200: someResponse
    //       422: validationError
    a.Router.HandleFunc("/products", a.getProducts).Methods("GET")
    a.Router.HandleFunc("/products", a.createProduct).Methods("POST")
    a.Router.HandleFunc("/products/{id:[0-9]+}", a.getProduct).Methods("GET")
    a.Router.HandleFunc("/products/{id:[0-9]+}", a.updateProduct).Methods("PUT")
    a.Router.HandleFunc("/products/{id:[0-9]+}", a.deleteProduct).Methods("DELETE")
}

func (a *App) Run() {
    loggedRouter := handlers.LoggingHandler(a.LogFile, a.Router)
    port := a.Config.Port
    log.Info("Starting server on port "+port+", environment "+a.Config.EnvType)
    log.Fatal(http.ListenAndServe(port, loggedRouter))
}
