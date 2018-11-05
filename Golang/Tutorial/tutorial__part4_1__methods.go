package main

import (
    "fmt"
    "math"
)

type Vertex struct {
    X, Y float64
}

func (v Vertex) Abs() float64 {
    // Go does not have classes. However, you can define methods on types.
    return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func Abs(v Vertex) float64 {
    // Remember: a method is just a function with a receiver argument.
    return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

type MyFloat float64

func (f MyFloat) Abs() float64 {
    // You can declare a method on non-struct types, too.
    // You can only declare a method with a receiver whose type is defined in the same package as the method. You cannot declare a method with a receiver whose type is defined in another package (which includes the built-in types such as int).

    if f < 0 {
        return float64(-f)
    }
    return float64(f)
}

func (v *Vertex) Scale(f float64) {
    // Methods with pointer receivers can modify the value to which the receiver points (as Scale does here). Since methods often need to modify their receiver, pointer receivers are more common than value receivers.

    v.X = v.X * f
    v.Y = v.Y * f
}

func Scale(v *Vertex, f float64) {
    v.X = v.X * f
    v.Y = v.Y * f
}

func main() {
    v := Vertex{3, 4}
    fmt.Println(v.Abs())
    fmt.Println(Abs(v))

    f := MyFloat(5.5)
    fmt.Println(f.Abs())

    // For the statement v.Scale(5), even though v is a value and not a pointer, the method with the pointer receiver is called automatically. That is, as a convenience, Go interprets the statement v.Scale(5) as (&v).Scale(5) since the Scale method has a pointer receiver.
    v.Scale(10)
    fmt.Println(v.Abs())
    p := &v
    p.Scale(10)
    fmt.Println(v.Abs())
    Scale(&v, 10)
    fmt.Println(v.Abs())

    // methods with value receivers take either a value or a pointer as the receiver when they are calle
    fmt.Println(v.Abs())
    p = &v
    fmt.Println(p.Abs())

    // There are two reasons to use a pointer receiver.
    // The first is so that the method can modify the value that its receiver points to.
    // The second is to avoid copying the value on each method call. This can be more efficient if the receiver is a large struct, for example.
    // In general, all methods on a given type should have either value or pointer receivers, but not a mixture of both.
}
