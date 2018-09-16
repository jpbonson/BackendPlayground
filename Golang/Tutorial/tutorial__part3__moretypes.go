package main

import (
	"fmt"
)

type Vertex struct {
    X int
    Y int
}

func pointerFunction() {
    //A pointer holds the memory address of a value.

    //The type *T is a pointer to a T value. Its zero value is nil.

    var p *int

    //The & operator generates a pointer to its operand.

    i := 42
    p = &i

    //The * operator denotes the pointer's underlying value.

    fmt.Println("pointer i: ", i)
    fmt.Println("pointer *p: ", *p) // read i through the pointer p
    *p = 21         // set i through the pointer p, This is known as "dereferencing" or "indirecting".
    fmt.Println("pointer i: ", i)
    fmt.Println("pointer *p: ", *p)
}

func testVertex() {
    vertex := Vertex{1, 2}
    fmt.Println("Vertex1: ", vertex)
    fmt.Println("Vertex.X: ", vertex.X)
    p := vertex // copy
    p.X = 5
    // To access the field X of a struct when we have the struct pointer p we could write (*p).X. However, that notation is cumbersome, so the language permits us instead to write just p.X, without the explicit dereference.
    fmt.Println("Vertex2: ", vertex)
    fmt.Println("p: ", p)
    q := &vertex // reference
    q.X = 10
    fmt.Println("Vertex3: ", vertex)
    fmt.Println("q: ", q)
    fmt.Println("*q: ", *q)
}

var (
    v1 = Vertex{1, 2}  // has type Vertex
    v2 = Vertex{X: 1}  // Y:0 is implicit
    v3 = Vertex{}      // X:0 and Y:0
    p  = &Vertex{1, 2} // has type *Vertex
)

func testArray() {
    var a [2]string
    a[0] = "Hello"
    a[1] = "World"
    fmt.Println("array: ", a[0], a[1])
    fmt.Println("array: ", a)
}

func testSlices() {
    primes := [6]int{2, 3, 5, 7, 11, 13}
    fmt.Println("primes: ", primes)

    var s []int = primes[1:4] // The type []T is a slice with elements of type T
    fmt.Println("primes[1:4]: ", s)
    x := primes[0:1]
    fmt.Println("primes[0:1]: ", x)
    // y := primes[0:-1] // invalid

    names := [4]string{
        "John",
        "Paul",
        "George",
        "Ringo",
    }
    fmt.Println("names: ", names)

    a := names[0:2]
    b := names[1:3]
    fmt.Println("a, b: ", a, b)

    b[0] = "XXX"
    fmt.Println("a, b: ", a, b)
    fmt.Println("names: ", names)
}

func main() {
    fmt.Println("Welcome to the playground, part 3!")

    pointerFunction()
    testVertex()
    fmt.Println("vertex vars: ", v1, v2, v3, p)
    testArray()
    testSlices()
}

// An array's length is part of its type, so arrays cannot be resized. This seems limiting, but don't worry; Go provides a convenient way of working with arrays.

// A slice, on the other hand, is a dynamically-sized, flexible view into the elements of an array. In practice, slices are much more common than arrays.
// Slices are like references to arrays
// A slice does not store any data, it just describes a section of an underlying array.
// Changing the elements of a slice modifies the corresponding elements of its underlying array.
// Other slices that share the same underlying array will see those changes.


// https://tour.golang.org/moretypes/9
