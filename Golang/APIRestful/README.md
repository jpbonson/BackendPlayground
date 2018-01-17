# RESTful API

## Install
```
go get
make install
```

## Run
```
make run
```

## Test
```
make test
```

## API

### Products

#### List products: GET /products
```
curl -X GET -H "Content-type: application/json" -H "Accept: application/json" localhost:8000/products
```

```
curl -X GET -H "Content-type: application/json" -H "Accept: application/json" localhost:8000/products?name=catalog
```

#### Get product: GET /products/:id
```
curl -X GET -H "Content-type: application/json" -H "Accept: application/json" localhost:8000/products/1
```

#### Create product: POST /products
```
curl -d '{"name":"catalog", "metadata":"{\"i18n\":{\"name\":{\"pt-BR\":\"Catalogo\",\"en\":\"Catalog\"}}}"}' -H "Content-Type: application/json" -X POST localhost:8000/products
```

#### Update product: PUT /products/:id
```
curl -d '{"name":"catalog", "metadata":"{\"i18n\":{\"name\":{\"pt-BR\":\"Catalogo\",\"en\":\"catalog\"}}}"}' -H "Content-Type: application/json" -X PUT localhost:8000/products/2
```

#### Remove product: DELETE /products/:id
```
curl -H "Content-Type: application/json" -X DELETE localhost:8000/products/2
```
