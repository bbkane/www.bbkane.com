+++
title = "Go Dependency Injection With Functions"
date = 2022-02-24
+++

I'm writing [warg](https://github.com/bbkane/warg) to parse my CLI apps. In some cases, I want to be able to read an environmental variable into a data structure. I started doing this and it worked fine:

```go
func Work() {
    // ... lots of code ...
    user, exists := os.LookupEnv("USER")
    // ... lots more code ...
}
```

Then I realized I needed to test my code...

Code depending on the environment directly like this makes tests more difficult because the test results are now also dependent on whats in the environment. This is especially difficult when the tests are parallelized. What if another test removes this environmental variable while this test is testing for it?

The classic and most obvious solution is to define an interface and two implementations - one that uses the environment, and one that lets me mock the environment, then parameterize `Work` with that interface:

```go
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

func Work(env EnvironLike) {
    // ... lots of code ...
    user, exists := env.Lookup("USER")
    // ... lots more code ...
}
```

Now I'm *injecting* the environment dependency instead of depending on it directly. A test can call `Work` with the dummy and not flake out if something changes with the environment:

```go
Work(DictEnviron(map[string]string{"USER": "me"}))
```

And application code can depend on the environment wrapper:

```go
Work(Environ{})
```

Unfortunately, the `Work` function has this odd `EnvironLike` parameter. It's more difficult to scan code using `Work` because I have to understand what an `Environ{}` even does. Before I were just looking at `os.LookupEnv`, which is pretty familiar because it's in Go's standard library.

Can I do better? Actually, yes!

Because I really only depend on the behavior of `os.LookupEnv`, I can declare a function type that matches `os.LookupEnv`'s arguments and return values, and depend on an instance of that type only. This means I don't need to wrap `os.LookupEnv` in a struct to use it - I can use `os.LookupEnv` directly and make each call site easier to read.

```go
type LookupFunc func(key string) (string, bool)

func DictLookup(m map[string]string) LookupFunc {
	return func(key string) (string, bool) {
		val, exists := m[key]
		return val, exists
	}
}

func Work(f LookupFunc) {
    // ... lots of code ...
    user, exists := f("USER")
    // ... lots more code ...
}
```

Test code can call `Work` with `DictLookup`:

```go
Work(DictLookup(map[string]string{"USER": "me"}))
```

And app code can use `os.LookupEnv`:

```go
Work(os.LookupEnv)
```

Less code, and it's easier to read! Win!

See a running example in [./lookup.go](./lookup.go) or the [Go Playground](https://go.dev/play/p/YlOxokcJAf4).
