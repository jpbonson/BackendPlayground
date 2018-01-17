run: build
	./authorization-service

.PHONY: test
test:
	go test -v ./test

build:
	go clean
	go build -o authorization-service

install: build
	go install
