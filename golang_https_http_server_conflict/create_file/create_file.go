package main

import (
	"log"
	"os"
	"time"
)

var filename = ""

func createFile(path string) {
	var _, err = os.Stat(path)
	if os.IsNotExist(err) {
		var file, err = os.Create(path)
		if err != nil {
			panic(err)
		}
		defer file.Close()
	}
}

func createA() {
	filename = "/tmp/a"
	createFile(filename)
	log.Println(filename)
}

func createB() {
	filename = "/tmp/b"
	createFile(filename)
	log.Println(filename)
}

func main() {
	go createA()
	// time.Sleep(1000 * time.Microsecond)
	go createB()

	for {
		time.Sleep(2 * time.Microsecond)
	}
}
