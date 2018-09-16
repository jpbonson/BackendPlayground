package main

import (
	"fmt"
    "math"
    "runtime"
    "time"
)

func forLoop() {
    sum := 0
    for i := 0; i < 10; i++ {
        sum += i
    }
    fmt.Println("loop1: ", sum)
}

func forLoopOmmitedParams() {
    sum := 1
    for sum < 10 { // while
        sum += sum
    }
    if v := math.Pow(2, 2); v < 100 {
        fmt.Println("if: ", v)
    }
    // fmt.Println("if: ", v) // undefined
    fmt.Println("loop2: ", sum)
}

func infiniteLoop() {
    a := 0
    for {
        if a == 0 {
            a += 1
        } else {
            a += 2
        }
        break
    }
    fmt.Println("loop3: ", a)
}

func switchFunction1() {
    fmt.Print("Go runs on ")
    switch os := runtime.GOOS; os {
    case "darwin":
        fmt.Println("OS X.")
    case "linux":
        fmt.Println("Linux.")
    default:
        fmt.Printf("%s.", os)
    }
}

func switchFunction2() {
    fmt.Println("When's Saturday?")
    today := time.Now().Weekday()
    switch time.Sunday {
    case today + 0:
        fmt.Println("Today.")
    case today + 1:
        fmt.Println("Tomorrow.")
    case today + 2:
        fmt.Println("In two days.")
    default:
        fmt.Println("Too far away.")
    }
}

func switchFunction3() {
    t := time.Now()
    switch {
    case t.Hour() < 12:
        fmt.Println("Good morning!")
    case t.Hour() < 17:
        fmt.Println("Good afternoon.")
    default:
        fmt.Println("Good evening.")
    }
}

func deferFunction() {
    fmt.Println("defer: counting")

    for i := 0; i < 5; i++ {
        defer fmt.Println("defer:", i)
    }

    fmt.Println("defer: done")
}

func main() {
    fmt.Println("Welcome to the playground, part 2!")
    forLoop()
    forLoopOmmitedParams()
    infiniteLoop()
    switchFunction1()
    switchFunction2()
    switchFunction3()
    deferFunction()
}

// Go's switch is like the one in C, C++, Java, JavaScript, and PHP, except that Go only runs the selected case, not all the cases that follow. In effect, the break statement that is needed at the end of each case in those languages is provided automatically in Go. Another important difference is that Go's switch cases need not be constants, and the values involved need not be integers.

// Defer
// A defer statement defers the execution of a function until the surrounding function returns.
// The deferred call's arguments are evaluated immediately, but the function call is not executed until the surrounding function returns.
// Deferred function calls are pushed onto a stack. When a function returns, its deferred calls are executed in last-in-first-out order.
