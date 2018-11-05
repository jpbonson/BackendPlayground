package main

import (
    "fmt"
    "math"
)

func main() {
    testInterfaces()
    testTypeAssertion()
    testSwitchType()
    testStringerInterface()
    testStringerInterface2()
}

type I interface {
    M()
}

type T struct {
    S string
}

func (t *T) M() {
    if t == nil {
        fmt.Println("<nil>")
        return
    }
    fmt.Println(t.S)
}

type F float64

func (f F) M() {
    fmt.Println(f)
}

func describe(i I) {
    fmt.Printf("describe(%v, %T)\n", i, i)
}

func genericDescribe(i interface{}) {
    fmt.Printf("genericDescribe(%v, %T)\n", i, i)
}

func testInterfaces() {
    // Interfaces are implemented implicitly
    // A type implements an interface by implementing its methods. There is no explicit declaration of intent, no "implements" keyword.
    // Implicit interfaces decouple the definition of an interface from its implementation, which could then appear in any package without prearrangement.
    // An interface value holds a value of a specific underlying concrete type.
    // Calling a method on an interface value executes the method of the same name on its underlying type.
    fmt.Println("\ntestInterfaces()")

    var i I

    i = &T{"Hello"}
    describe(i)
    i.M()

    i = F(math.Pi)
    describe(i)
    i.M()


    // If the concrete value inside the interface itself is nil, the method will be called with a nil receiver.
    // In some languages this would trigger a null pointer exception, but in Go it is common to write methods that gracefully handle being called with a nil receiver
    // Note that an interface value that holds a nil concrete value is itself non-nil.
    var t *T
    i = t
    describe(i)
    i.M()


    // A nil interface value holds neither value nor concrete type.
    // Calling a method on a nil interface is a run-time error because there is no type inside the interface tuple to indicate which concrete method to call.
    var x I
    describe(x)
    // x.M()


    // The interface type that specifies zero methods is known as the empty interface: interface{}
    // An empty interface may hold values of any type. (Every type implements at least zero methods.)
    // Empty interfaces are used by code that handles values of unknown type. For example, fmt.Print takes any number of arguments of type interface{}.
    var y interface{}
    genericDescribe(y)

    y = 42
    genericDescribe(y)

    y = "hello"
    genericDescribe(y)
}

func testTypeAssertion() {
    // A type assertion provides access to an interface value's underlying concrete value.
    fmt.Println("\ntestTypeAssertion()")

    var i interface{} = "hello"
    fmt.Println(i)

    s := i.(string)
    fmt.Println(s)

    s, ok := i.(string)
    fmt.Println(s, ok)

    f, ok := i.(float64)
    fmt.Println(f, ok)

    // f = i.(float64) // panic
    // fmt.Println(f)
}

func testSwitchType() {
    fmt.Println("\ntestSwitchType()")
    do(21)
    do("hello")
    do(true)
}

func do(i interface{}) {
    switch v := i.(type) {
    case int:
        fmt.Printf("Twice %v is %v\n", v, v*2)
    case string:
        fmt.Printf("%q is %v bytes long\n", v, len(v))
    default:
        fmt.Printf("I don't know about type %T!\n", v)
    }
}

type Person struct {
    Name string
    Age  int
}

func (p Person) String() string {
    return fmt.Sprintf("%v (%v years)", p.Name, p.Age)
}

// type Stringer interface {
//     String() string
// }

func testStringerInterface() {
    // A Stringer is a type that can describe itself as a string. The fmt package (and many others) look for this interface to print values.

    fmt.Println("\ntestStringerInterface()")
    a := Person{"Arthur Dent", 42}
    z := Person{"Zaphod Beeblebrox", 9001}
    fmt.Println(a, z)
}

type IPAddr [4]byte

func (a IPAddr) String() string {
    return fmt.Sprintf("%v.%v.%v.%v", a[0], a[1], a[2], a[3])
}

func testStringerInterface2() {
    fmt.Println("\ntestStringerInterface2()")

    hosts := map[string]IPAddr{
        "loopback":  {127, 0, 0, 1},
        "googleDNS": {8, 8, 8, 8},
    }
    for name, ip := range hosts {
        fmt.Printf("%v: %v\n", name, ip)
    }
}

// https://tour.golang.org/methods/19
