package main

import (
	"fmt"
	"math"
	"math/cmplx"
	"math/rand"
	"time"
)

var c, python, java bool

var (
	ToBe   bool       = false
	MaxInt uint64     = 1<<64 - 1
	z      complex128 = cmplx.Sqrt(-5 + 12i)
)

const Blah = 3.14
const Bleh = "bleh"

func add(x int, y int) int {
	return x + y
}

func add2(x, y int) int {
	return x + y
}

func swap(x, y string) (string, string) {
	return y, x
}

func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}

func main() {
	fmt.Println("Welcome to the playground!")

	fmt.Println("The time is", time.Now())

	fmt.Println("My favorite number is", rand.Intn(10))

	fmt.Printf("Now you have %g problems.\n", math.Sqrt(7))

	fmt.Println("math.Pi ", math.Pi)

	fmt.Println("add(42, 13) ", add(42, 13))

	fmt.Println("add2(42, 13) ", add2(42, 13))

	a, b := swap("hello", "world")
	fmt.Println("swap('hello', 'world') ", a, b)

	x, y := split(17)
	fmt.Println("split(17) ", x, y)

	fmt.Println("bool initialized global vars ", c, python, java)

	var i, j int = 1, 2
	var q, w = true, "no!"
	k := 3
	var blah string
	fmt.Println("local vars ", i, j, q, w, k, blah)

	fmt.Printf("Type: %T Value: %v\n", ToBe, ToBe)
	fmt.Printf("Type: %T Value: %v\n", MaxInt, MaxInt)
	fmt.Printf("Type: %T Value: %v\n", z, z)

	i = 42
	l := float64(i)
	fmt.Println("conversão de números ", i, l)

	fmt.Println("conts ", Blah, Bleh)
}

// go run tutorial__part1__basic.go

// PACKAGES
// - Every Go program is made up of packages.
// - Programs start running in package main.
// - By convention, the package name is the same as the last element of the import
// path. For instance, the "math/rand" package comprises files that begin with the
// statement package rand.
// - In Go, a name is exported if it begins with a capital letter.

// ASSIGNMENT
// - In Go, := is for declaration + assignment, whereas = is for assignment only.
// - For example, var foo int = 10 is the same as foo := 10.
//
// - Outside a function, every statement begins with a keyword (var, func, and
// so on) and so the := construct is not available.

// TYPES
// - bool
// - string
// - int  int8  int16  int32  int64 uint uint8 uint16 uint32 uint64 uintptr
// - byte // alias for uint8
// - rune // alias for int32, represents a Unicode code point
// - float32 float64
// - complex64 complex128
