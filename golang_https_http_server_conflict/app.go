package main

import (
	"log"
	"net"
	"net/http"
	"time"
)

func handler(w http.ResponseWriter, req *http.Request) {
	w.Header().Set("Content-Type", "text/plain")
	w.Write([]byte("This is an example server.\n"))
}

var Server *http.Server
var addr = ""

func runHTTPS() {
	addr = ":2233"
	http.HandleFunc("/", handler)
	log.Println("https://127.0.0.1:2233/")
	err := http.ListenAndServeTLS(addr, "cert.pem", "private.pem", nil)
	if err != nil {
		panic(err)
	}
}

func runHTTP() {
	addr = ":8082"
	log.Println("http://127.0.0.1:8082/")
	ln, err := net.Listen("tcp4", addr)
	if err != nil {
		panic(err)
	}
	log.Println(ln)
}

func main() {

	go runHTTPS()
	// time.Sleep(1000 * time.Microsecond)
	go runHTTP()

	for {
		time.Sleep(2 * time.Microsecond)
	}
}
