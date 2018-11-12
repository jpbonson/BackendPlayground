package main

import (
    "fmt"
    "time"
)

func say(s string) {
    for i := 0; i < 5; i++ {
        time.Sleep(100 * time.Millisecond)
        fmt.Println(s)
    }
}

func sayNoSleep(s string) {
    for i := 0; i < 5; i++ {
        fmt.Println(s)
    }
}

func testGoroutine() {
    // A goroutine is a lightweight thread managed by the Go runtime.
    // go f(x, y, z) starts a new goroutine running f(x, y, z)
    // The evaluation of f, x, y, and z happens in the current goroutine and the execution of f happens in the new goroutine.
    // Goroutines run in the same address space, so access to shared memory must be synchronized. The sync package provides useful primitives, although you won't need them much in Go as there are other primitives.

    go sayNoSleep("with goroutine (no sleep)")
    sayNoSleep("without goroutine (no sleep)")
    go say("with goroutine")
    say("without goroutine")
}

func main() {
    testGoroutine()
}

// https://tour.golang.org/concurrency/1
