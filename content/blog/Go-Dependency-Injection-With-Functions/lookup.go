package main

import (
	"fmt"
	"os"
)

// -- func

type LookupFunc func(key string) (string, bool)

func DictLookup(m map[string]string) LookupFunc {
	return func(key string) (string, bool) {
		val, exists := m[key]
		return val, exists
	}
}

// -- interface

type EnvironLike interface {
	Lookup(key string) (string, bool)
}

type Environ struct{}

func (Environ) Lookup(key string) (string, bool) {
	return os.LookupEnv(key)
}

type DictEnviron map[string]string

func (d DictEnviron) Lookup(key string) (string, bool) {
	res, exists := d[key]
	return res, exists
}

func main() {
	{
		var f LookupFunc
		f = os.LookupEnv
		f = DictLookup(map[string]string{"USER": "me"})
		user, exists := f("USER")
		fmt.Println(user, exists)
	}
	{
		var e EnvironLike
		e = Environ{}
		e = DictEnviron(map[string]string{"USER": "me"})
		user, exists := e.Lookup("USER")
		fmt.Println(user, exists)
	}

}
