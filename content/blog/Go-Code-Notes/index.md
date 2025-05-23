+++
title = "Go Code Notes"
date = 2023-12-27
aliases = [ "2018/09/04/Go-Notes.html" ]

+++

These are notes on writing good Go Code. Also see [Go Developer Tooling](@/blog/Go-Developer-Tooling/index.md). and [Go Project Notes](@/blog/Go-Project-Notes/index.md)

# Testing

Some notes on testing in Go. A lot of these notes came from [Advanced Testing in Go (Hashimoto)](https://www.youtube.com/watch?v=8hQG7QlcLBk) ([transcipt](https://about.sourcegraph.com/go/advanced-testing-in-go)).

## Types of tests

Copied from [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) except where noted.

- **Unit tests** - Your unit  tests make sure that a certain unit (your *subject under test*) of your  codebase works as intended. Unit tests have the narrowest scope of all the  tests in your test suite. The number of unit tests in your test suite will  largely outnumber any other type of test.
- **Integration tests** - test the integration of your application with all the parts  that live outside of your application.
- **Contract tests** - make sure that the implementations on the consumer and provider side still stick to the defined contract. (also see [Working without mocks](https://quii.gitbook.io/learn-go-with-tests/testing-fundamentals/working-without-mocks)).
- **UI tests** - testing UI code
- **End-to-End tests** - Testing your deployed application via its user interface. As they are complicated, they can be flaky and slow. (overlaps with acceptance tests)
- **Acceptance tests** - test that your software works correctly from a *user's* perspective, not just from a technical perspective - also see [Introduction to acceptance tests](https://quii.gitbook.io/learn-go-with-tests/testing-fundamentals/intro-to-acceptance-tests)
- **Fuzz tests** - See [Go Fuzzing](https://go.dev/doc/security/fuzz/) - a type of automated testing which continuously manipulates inputs to a program to find bugs. Relies on asserting properties about the code under test.

## Types of test doubles

Copied from [Working without mocks](https://quii.gitbook.io/learn-go-with-tests/testing-fundamentals/working-without-mocks) (and this whole online book is excellent).

- **Stubs** return the same canned data every time they are called
- **Spies** are like stubs but also record how they were called so the test can assert that the SUT calls the dependencies in specific ways.
- **Mocks** are like a superset of the above, but they only respond with specific data to specific invocations. If the SUT calls the dependencies with the wrong arguments, it'll typically panic.
- **Fakes** are like a genuine version of the dependency but implemented in a way more suited to fast running, reliable tests and local development. Often, your system will have some abstraction around persistence, which will be implemented with a database, but in your tests, you could use an in-memory fake instead.

## Testing private and public APIs

Test files for a package's publicly visible API should be named `<package>_ext_test.go` and start with `package <package>_test`.

Test files for a package's internal API should be named `<package>_int_test.go` and start with `package <package>`

## Comparison naming convention

Go's `testing` library wants you to do a lot of comparisons. The naming convention I want to use for these comparisons (taken from `testify`) is to call the value that I expect `expectedXXX` and always put it on the left side of the comparison,  and the value that I actually got `actualXXX`, and always put it on the right side of the comparison:

```go
if expectedThing != actualThing {
    t.Fatalf("Oopsie")
}
```

## Degrees of failure

The `testing` library has a couple ways to fail:

- `Fail` marks the current test as failed, but continues the execution of the current test.
- `Error/Errorf` is equivalent to `Log/Logf` followed by `Fail`.
- `FailNow` marks the current test as failed, and stops execution of the current test.
- `Fatal/Fatalf` is equivalent to `Log/Logf` followed by `FailNow`.

## [`testify`](https://github.com/stretchr/testify)

`testify` is super nice for comparing things because it writes most of my `if` statements for me. I can do:

```go
// Mark current test as failed, but continue current test
assert.Equal(t, expectedValue, actualValue)

// Mark current test as failed, exit current test
require.Equal(t, expectedValue, actualValue)
```

##  Table driven tests

Test the same logic on different data!

Here's a simple example - note that in lieu of testing what's in the potential error, I simply assert that it's nil or not nil. For this particular test, this is "enough" to satisfy me. Other tests might require more detailed comparisons.

```go
package main

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/require"
)

func AddOne(a int) (int, error) {
	if a == 3 {
		return 0, errors.New("We don't like the number 3")
	}
	return a + 1, nil
}

func TestAddOne(t *testing.T) {
	tests := []struct {
		name        string
		a           int
		expectedSum int
		expectedErr bool
	}{
		{name: "first", a: 1, expectedSum: 2, expectedErr: false},
		{name: "second", a: 2, expectedSum: 4, expectedErr: false},
		{name: "third", a: 3, expectedSum: 0, expectedErr: true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			actualSum, actualErr := AddOne(tt.a)
			if tt.expectedErr {
				require.Error(t, actualErr)
			} else {
				require.NoError(t, actualErr)
			}
			require.Equal(t, tt.expectedSum, actualSum)
		})
	}
}
```

When run, we see that the function is incorrect for the test data provided (or, more likely in this case, we need to correct the test data). `testify` gives us a super helpful error message.

```
$ go test ./...
--- FAIL: TestAddOne (0.00s)
    --- FAIL: TestAddOne/second (0.00s)
        main_test.go:37:
            	Error Trace:	main_test.go:37
            	Error:      	Not equal:
            	            	expected: 4
            	            	actual  : 3
            	Test:       	TestAddOne/second
FAIL
FAIL	github.com/bbkane/hello_testing	0.173s
FAIL
```

## Data files

When a test depends on a data file, Go will read it from a file path relative to the test. I like to stick my files for a test in a `testdata/TestName.xxx` file right next to the test. Then, within the test, I can `ioutil.Readfile('testdata/TestName.xxx')` to get the data. If each sub test in a table-driven test, needs a file, then I use `testdata/TestName/SubTestName.xxx`.

## Golden files

Sometimes, I want to test that a function outputs the correct bytes - like a file, an HTTP response, or the `--help` output from the CLI parsing library I'm writing. In these cases, it's helpful to make the tests read an environmental variable, and write the bytes to a file when it is passed. Then I can manually read those files to ensure correctness, commit them, and make the test check the bytes generated to the file when the environmental variable is not set. My usage of this term comes from [Advanced Testing in Go (Hashimoto)](https://www.youtube.com/watch?v=8hQG7QlcLBk), but I've also seen it called "snapshot" testing.

### Golden file example (`logos`)

See [logos](https://github.com/bbkane/logos/blob/fcff1df203a5fdee193269be19de53383c7ac5e2/logos_ext_test.go) for an example. I still haven't decided whether to turn this into a library or simply copy-paste it wherever.

## Example tests

Code examples can be added to tests and also show up in the docs! See [the Go blog](https://go.dev/blog/examples) for more details, or see my example below:

```go
package main_test

import "fmt"

func ExampleExample() {
	fmt.Println("hello!")
	// Output: hello!
}
```

# Errors

To some extent these error creation/handling ideas are tested in `warg` and other code, but I still have yet to prove other ideas. In particular, when prototyping I can get quite far eschewing these ideas and just using `fmt.Errorf` for everything, but `fmt.Errorf` errors can ossify in my project as it matures.

## Guidelines

- An error should consist of a unique (to the repo) message and optionally more information specific to the problem. The message should be unique because Go errors do not include file information such as line numbers, so you need to grep for the error. Example: `ChoiceNotFound{Msg: "choice not found", Choices: []string{"a", "b", "c"}}`.
- Errors should not include information the caller already knows. Example: in `ChoiceNotFound` above, the error does not need to contain the choice sent to the function that returns it because the caller already knows it.
- Errors that do not need to include extra information can just use a package level sentinel `errors.New(...)` var. Example: `var ErrIncompatibleInterface = errors.New("could not decode interface into Value")`.
- Errors that do need to include extra information should not jam that into `fmt.Errorf`, but instead use a struct with an `Error()` method so the caller can retrieve the extra info.
- Propagate errors by wrapping them - either with `fmt.Errorf` (if you don't need to add more unique context), or with a struct using an `Unwrap` method (if you do need more unique context).

## Unsolved problems and tradeoffs

- I wish errors had more file information like line numbers for debugging purposes. There ARE packages to add this, but I haven't chosen one.
- Error wrapping allows you to produce errors with one wrapped "child" error (like a chain of errors), but sometimes you'd like to produce an error with more than one "children" errors (like a tree of errors). An example of this is parsing, where you'd like to parse as much as you can and produce all the useful errors you can, so the user can fix all of those at once before they try to parse again. Once. again, there are packages to solve this, and some declined stdlib proposals like [proposal: errors: add With(err, other error) error · Issue #52607 · golang/go](https://github.com/golang/go/issues/52607).
- The approach above almost completely ignores API evolution concerns. In particular, what if I have a sentinel error, and the code changes, and I now need to add context to it? I'd need to change the type, which breaks the API. See [Don’t just check errors, handle them gracefully | Dave Cheney](https://dave.cheney.net/2016/04/27/dont-just-check-errors-handle-them-gracefully) for a great description of these problems and solutions. NOTE that this post precedes Go 1.13's error wrapping functions, which can (imo) be used to replace his `errors` library. No one uses my code, and I'm not the smartest man, so I've chosen simplicity of implementation with the possibility of API breakage over more complex but fewer API-breaking error implementations. I want to note this tradeoff explicitly as it's not the correct tradeoff for more public code.

## References

- [Working with Errors in Go 1.13 - The Go Programming Language](https://go.dev/blog/go1.13-errors) - describes the mechanics of wrapping errors.
- [Wrapping Errors the Right Way - by Hunter Herman](https://errnil.substack.com/p/wrapping-errors-the-right-way) - advocates for only including information the caller doesn't have.
- [Designing error types in Rust](https://mmapped.blog/posts/12-rust-error-handling.html) is about Rust, but it advocates a couple ideas I really like, in particular the difference between libraries and applications, as well as that it's difficult to "overspecify" errors: "Feel free to introduce distinct error types for each function you implement. I am still looking for Rust code that went overboard with distinct error types."
- [command center: Error handling in Upspin](https://commandcenter.blogspot.com/2017/12/error-handling-in-upspin.html) talks about Rob Pike's approach to errors in Upspin. Among other things, it talks about the tension between using errors to signal to users and to help programmers debug, as well as "operational traces" vs the more conventional stack traces other languages use. It also highlights that different projects *should* handle errors differently. Also see [Failure is your Domain | Middlemost Systems](https://middlemost.com/failure-is-your-domain/) for more thoughts on this blog post, as well as comparisonts to other ways to handle errors.
- [Error Handling in Rust - Andrew Gallant's Blog](https://blog.burntsushi.net/rust-error-handling/#the-short-story) - another Rust post, but it talks about error combinators, which might be useful to implement for some projects.

# Tools

## Generate Call graphs with [`crabviz`](https://github.com/chanhx/crabviz)

This might not be strictly more useful than "Show call heirarchy", but I'm having a lot of fun with the VS Code extension!

## Visualize package imports with [gopkgview](https://github.com/grishy/gopkgview)

I find `gopkgview` useful to see issues (or the lack thereof) with my package imports. As a positive example, here's the import diagram of [`envelope`](https://github.com/bbkane/envelope):



![image-20250120202741319](./index.assets/image-20250120202741319.png)

I was going for a somewhat layered architecture here, and that's clearly visible:

- the "presentation" layer (`cli` ) imports some helpers (`tableprint`), but uses the `app` package to talk to the storage packages (`sqliteconnect` , `sqlcgen`). The `app` package is the only user of the storage packages
- the `cli`, `tableprint`, and `app` packages use the shared set of types in the `models` package to interface with each other. For example,  to do a create operation, the `cli` parses `os.Args` and instantiates a `models.CreateXxxArgs` and passes it to the `app` package. The `app` package creates an `Xxx`, then hands it back to `cli`. `cli`, then hands the `Xxx` to `tableprint` to print. 

Now, whether a layered architecture like this is worth the trouble is another conversation (expand below for that tangent), but the point is that I can analyze dependencies quite easily with this tool to investigate architecture issues.

There's also [modgraphviz](https://pkg.go.dev/golang.org/x/exp/cmd/modgraphviz), which outputs a [graphviz](https://dreampuf.github.io/GraphvizOnline/) graph, but I'm not a huge fan of the auto-layout and filtering options.

<details>

TODO: move this to its own blog post...

Theoretical benefits I probably won't utilize for this project:

- I'm not planning on switching out another CLI library,  or the sql bits, so I'm not sure they need to be self-contained.
- This project is small enough that I have confidence in correctness using mostly integration tests, so I don't need a ton of separation between packages for testing

Actual/planned benefits:

- I feel like everything is nicely structured and almost everything "has a home". There are a few helper functions in the `models` package, but 🤷.
- I can fairly easily insert observability tooling "between" the layers. For example, to log every sql statement, I only have to mess with the app -> sql interface . Similarly, to log all CLI commands, I only have to mess with the CLI -> app interface. I don't need caching, but that would also be straightforward.
- I wrote this app to use for my projects, but ALSO to get experience with this architecture in a solo project. Projects at work already have an architecture and are always too big (and involve convincing teammates and postponing other work) to change things whenever I want to try a new pattern.

Actual drawbacks

- Large amounts of the code in this project are translating at the layers - to create an `Xxx`, I define CLI flags for it, separately define an app-level `CreateXxxArgs` for it, separately define (actually generate with `sqlc`) a storage layer `CreateXxxArgs` for it, then do the same thing in reverse to fill out the `models.Xxx` struct before passing it to `tableprint`. This makes it a slog to build more commands and especially depressing to prototype them- if I want to add a new command (say `xxx delete`), I'm writing lots of structs and translation code...

Maybe for the next project I'll try the "vertical slice" architecture folks find so freeing...

</details>

# Doc comment syntax examples

From [Go Doc Comments - The Go Programming Language](https://golang.org/doc/comment#syntax), a large doc with lots of great advice, none of which I seem to miss remembering more than how to make links and lists work in the weird "almost markdown" comment syntax. I'm mostly copying the code examples and not the larger explanation.

## Notes

```go
// TODO(user1): refactor to use standard library context
// BUG(user2): not cleaned up
var ctx context.Context
```

## Deprecations

```go
// Reset zeros the key data and makes the Cipher unusable.
//
// Deprecated: Reset can't guarantee that the key will be entirely removed from
// the process's memory.
func (c *Cipher) Reset()
```

## Headings

```go
// Package strconv implements conversions to and from string representations
// of basic data types.
//
// # Numeric Conversions
//
// The most common numeric conversions are [Atoi] (string to int) and [Itoa] (int to string).
...
package strconv
```

## Links

```go
// Package json implements encoding and decoding of JSON as defined in
// [RFC 7159]. The mapping between JSON and Go values is described
// in the documentation for the Marshal and Unmarshal functions.
//
// For an introduction to this package, see the article
// “[JSON and Go].”
//
// [RFC 7159]: https://tools.ietf.org/html/rfc7159
// [JSON and Go]: https://golang.org/doc/articles/json_and_go.html
package json
```

## Doc links

```go
package bytes

// ReadFrom reads data from r until EOF and appends it to the buffer, growing
// the buffer as needed. The return value n is the number of bytes read. Any
// error except [io.EOF] encountered during the read is also returned. If the
// buffer becomes too large, ReadFrom will panic with [ErrTooLarge].
func (b *Buffer) ReadFrom(r io.Reader) (n int64, err error) {
    ...
}
```

NOTE: When referring to other packages, “pkg” can be either a full import path or the assumed package name of an existing import. The assumed package name is either the identifier in a renamed import or else [the name assumed by goimports](https://pkg.go.dev/golang.org/x/tools/internal/imports#ImportPathToAssumedName). There are a few more caveats, see [here](https://go.dev/doc/comment#doclinks) if this isn't rendering correctly.

## Lists

```go
package url

// PublicSuffixList provides the public suffix of a domain. For example:
//   - the public suffix of "example.com" is "com",
//   - the public suffix of "foo1.foo2.foo3.co.uk" is "co.uk", and
//   - the public suffix of "bar.pvt.k12.ma.us" is "pvt.k12.ma.us".
//
// Implementations of PublicSuffixList must be safe for concurrent use by
// multiple goroutines.
//
// An implementation that always returns "" is valid and may be useful for
// testing but it is not secure: it means that the HTTP server for foo.com can
// set a cookie for bar.com.
//
// A public suffix list implementation is in the package
// golang.org/x/net/publicsuffix.
type PublicSuffixList interface {
    ...
}
```

NOTE: nested lists are not supported

## Code Blocks

```go
package sort

// Search uses binary search...
//
// As a more whimsical example, this program guesses your number:
//
//  func GuessingGame() {
//      var s string
//      fmt.Printf("Pick an integer from 0 to 100.\n")
//      answer := sort.Search(100, func(i int) bool {
//          fmt.Printf("Is your number <= %d? ", i)
//          fmt.Scanf("%s", &s)
//          return s != "" && s[0] == 'y'
//      })
//      fmt.Printf("Your number is %d.\n", answer)
//  }
func Search(n int, f func(int) bool) int {
    ...
}
```

