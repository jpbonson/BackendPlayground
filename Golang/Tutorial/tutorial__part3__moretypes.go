package main

import (
	"fmt"
    "strings"
)

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
    type Vertex struct {
        X int
        Y int
    }

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

    var (
        v1 = Vertex{1, 2}  // has type Vertex
        v2 = Vertex{X: 1}  // Y:0 is implicit
        v3 = Vertex{}      // X:0 and Y:0
        v  = &Vertex{1, 2} // has type *Vertex
    )
    fmt.Println("vertex vars: ", v1, v2, v3, v)
}

func testArray() {
    // An array's length is part of its type, so arrays cannot be resized. This seems limiting, but don't worry; Go provides a convenient way of working with arrays.

    var a [2]string
    a[0] = "Hello"
    a[1] = "World"
    fmt.Println("array: ", a[0], a[1])
    fmt.Println("array: ", a)
}

func testSlices() {
    // A slice, on the other hand, is a dynamically-sized, flexible view into the elements of an array. In practice, slices are much more common than arrays.
    // Slices are like references to arrays
    // A slice does not store any data, it just describes a section of an underlying array.
    // Changing the elements of a slice modifies the corresponding elements of its underlying array.
    // Other slices that share the same underlying array will see those changes.

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

func testSlices2() {
    // This is an array literal:
    array := [3]bool{true, true, false}
    fmt.Println("array: ", array)
    // And this creates the same array as above, then builds a slice that references it:
    slice := []bool{true, true, false}
    fmt.Println("slice: ", slice)

    s := []struct {
        i int
        b bool
    }{
        {2, true},
        {3, false},
        {5, true},
        {7, true},
        {11, false},
        {13, true},
    }
    fmt.Println("slice struct: ", s)
}

func testSliceDefaults() {
    a := []int{2, 3, 5, 7, 11}

    // these slice expressions are equivalent:
    fmt.Println("a[0:5]: ", a[0:5])
    fmt.Println("a[:5]: ", a[:5])
    fmt.Println("a[0:]: ", a[0:])
    fmt.Println("a[:]: ", a[:])
}

func testSliceModification() {
    // A slice has both a length and a capacity.
    // The length of a slice is the number of elements it contains.
    // The capacity of a slice is the number of elements in the underlying array, counting from the first element in the slice.
    // The length and capacity of a slice s can be obtained using the expressions len(s) and cap(s).
    // You can extend a slice's length by re-slicing it, provided it has sufficient capacity. Try changing one of the slice operations in the example program to extend it beyond its capacity and see what happens.

    s := []int{2, 3, 5, 7, 11, 13}
    fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)

    // Slice the slice to give it zero length.
    s = s[:0]
    fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)

    // Extend its length.
    s = s[:4]
    fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)

    // Drop its first two values.
    s = s[2:]
    fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)
}

func testNilSlice() {
    // A nil slice has a length and capacity of 0 and has no underlying array.
    var s []int
    fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)
    if s == nil {
        fmt.Println("nil!")
    }
}

func testMakeSlice() {
    // Slices can be created with the built-in make function; this is how you create dynamically-sized arrays.
    // The make function allocates a zeroed array and returns a slice that refers to that array:
    x := make([]int, 5)  // len(a)=5
    fmt.Printf("%s len=%d cap=%d %v\n",
        "x", len(x), cap(x), x)

    // To specify a capacity, pass a third argument to make:
    y := make([]int, 0, 5) // len(b)=0, cap(b)=5
    fmt.Printf("%s len=%d cap=%d %v\n",
        "y", len(y), cap(y), y)

    y = y[:cap(y)] // len(b)=5, cap(b)=5
    fmt.Printf("%s len=%d cap=%d %v\n",
        "y", len(y), cap(y), y)

    y = y[1:]      // len(b)=4, cap(b)=4
    fmt.Printf("%s len=%d cap=%d %v\n",
        "y", len(y), cap(y), y)

    a := make([]int, 5)
    fmt.Printf("%s len=%d cap=%d %v\n",
        "a", len(a), cap(a), a)

    b := make([]int, 0, 5)
    fmt.Printf("%s len=%d cap=%d %v\n",
        "b", len(b), cap(b), b)

    c := b[:2]
    fmt.Printf("%s len=%d cap=%d %v\n",
        "c", len(c), cap(c), c)

    d := c[2:5]
    fmt.Printf("%s len=%d cap=%d %v\n",
        "d", len(d), cap(d), d)
}

func testMatrix() {
    // Create a tic-tac-toe board.
    board := [][]string{
        []string{"_", "_", "_"},
        []string{"_", "_", "_"},
        []string{"_", "_", "_"},
    }

    // The players take turns.
    board[0][0] = "X"
    board[2][2] = "O"
    board[1][2] = "X"
    board[1][0] = "O"
    board[0][2] = "X"

    for i := 0; i < len(board); i++ {
        fmt.Printf("%s\n", strings.Join(board[i], " "))
    }
}

func testAppend() {
    fmt.Println("\ntestAppend()")

    var s []int
    fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)

    // append works on nil slices.
    s = append(s, 0)
    fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)

    // The slice grows as needed.
    s = append(s, 1)
    fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)

    // We can add more than one element at a time.
    s = append(s, 2, 3, 4)
    fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)
}

func testIterateSlice() {
    fmt.Println("\ntestIterateSlice()")

    var pow = []int{1, 2, 4}
    for i, v := range pow {
        fmt.Printf("2**%d = %d\n", i, v)
    }

    for i := range pow {
        pow[i] = 1 << uint(i) // == 2**i
    }
    for _, value := range pow {
        fmt.Printf("%d\n", value)
    }
}

func testMap() {
    // A map maps keys to values.
    // The zero value of a map is nil. A nil map has no keys, nor can keys be added.
    // The make function returns a map of the given type, initialized and ready for use.

    fmt.Println("\ntestMap()")

    type Vertex struct {
        Lat, Long float64
    }

    var m map[string]Vertex

    m = make(map[string]Vertex)
    m["Bell Labs"] = Vertex{
        40.68433, -74.39967,
    }
    fmt.Println(m["Bell Labs"])
    fmt.Println(m)
}

func main() {
    fmt.Println("Welcome to the playground, part 3!")

    pointerFunction()
    testVertex()
    testArray()
    testSlices()
    testSlices2()
    testSliceDefaults()
    testSliceModification()
    testNilSlice()
    testMakeSlice()
    testMatrix()
    testAppend()
    testIterateSlice()
    testMap()
}

// https://tour.golang.org/moretypes/19
