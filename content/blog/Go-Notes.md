+++
title = "Go Notes"
date = 2018-09-04
updated = 2021-10-02
aliases = [ "2018/09/04/Go-Notes.html" ]
+++

These are things I want to remember in Go

## Notes on Testing

Some notes on testing in Go. A lot of these notes came from [Advanced Testing in Go (Hashimoto)](https://www.youtube.com/watch?v=8hQG7QlcLBk) ([transcipt](https://about.sourcegraph.com/go/advanced-testing-in-go)).

### Testing Private and Public APIs

Test files for a package's publicly visible API should be named `<package>_ext_test.go` and start with `package <package>_test`.

Test files for a package's internal API should be named `<package>_int_test.go` and start with `package <package>`

### Comparing Values Naming Convention

Go's `testing` library wants you to do a lot of comparisons. The naming convention I want to use for these comparisons (taken from `testify`) is to call the value that I expect `expectedXXX` and always put it on the left side of the comparison,  and the value that I actually got `actualXXX`, and always put it on the right side of the comparison:

```go
if expectedThing != actualThing {
    t.Fatalf("Oopsie")
}
```

### Degrees of Failure

The `testing` library has a couple ways to fail:

`Fail` marks the current test as failed, but continues the execution of the current test.

`Error/Errorf` is equivalent to `Log/Logf` followed by `Fail`.

`FailNow` marks the current test as failed, and stops execution of the current test.

`Fatal/Fatalf` is equivalent to `Log/Logf` followed by `FailNow`.

### testify

`testify` is super nice for comparing things because it writes most of my `if` statements for me. I can do:

```go
// Mark current test as failed, but continue current test
assert.Equal(t, expectedValue, actualValue)

// Mark current test as failed, exit current test
require.Equal(t, expectedValue, actualValue)
```

###  Table Driven Tests

Test the same logic on different data!

Here's a simple example - note that in lieu of testing what's in the potential error, I simply assert that it's nil or not nil. For this particular, this is "enough" to satisfy me. Other tests might require more detailed comparisons.

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
				require.NotNil(t, actualErr)
			} else {
				require.Nil(t, actualErr)
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

### Data Files

When a test depends on a data file, Go will read it from a file path relative to the test. I like to stick my files for a test in a `testdata/TestName.xxx` file right next to the test. Then, within the test, I can `ioutil.Readfile('testdata/TestName.xxx')` to get the data. If each sub test in a table-driven test, needs a file, then I use `testdata/TestName/SubTestName.xxx`.

### Golden Files

Sometimes, I want to test that a function outputs the correct bytes - like a file, an HTTP response, or the `--help` output from the CLI parsing library I'm writing. In these cases, it's helpful to make the tests take an `-update` flag, and write the bytes to a file when it is passed. Then I can manually read those files to ensure correctness, commit them, and make the test check the bytes generated to the file when the `-update` flag is not passed. An example:

```go
package main_test

import (
	"bytes"
	"flag"
	"io"
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/require"
)

func Write(w io.Writer) error {
	_, err := w.Write([]byte("hola\n"))
	return err
}

var update = flag.Bool("update", false, "update golden files")

func TestWrite(t *testing.T) {
	var actualBuffer bytes.Buffer
	actualErr := Write(&actualBuffer)
	require.Nil(t, actualErr)

	golden := filepath.Join("testdata", t.Name()+".golden.txt")
	if *update {
		mkdirErr := os.MkdirAll("testdata", 0700)
		require.Nil(t, mkdirErr)
		writeErr := ioutil.WriteFile(golden, actualBuffer.Bytes(), 0600)
		require.Nil(t, writeErr)
		t.Logf("Wrote: %v\n", golden)
	}

	expectedBytes, readErr := ioutil.ReadFile(golden)
	require.Nil(t, readErr)

	require.Equal(t, expectedBytes, actualBuffer.Bytes())
}
```

When running this test the first time, I get the following error:

```
$ go test golden_test.go
--- FAIL: TestWrite (0.00s)
    golden_test.go:37:
        	Error Trace:	golden_test.go:37
        	Error:      	Expected nil, but got: &fs.PathError{Op:"open", Path:"testdata/TestWrite.golden.txt", Err:0x2}
        	Test:       	TestWrite
FAIL
FAIL	command-line-arguments	0.095s
FAIL
```

However, I can then use the `-update` flag to write the file (I'm also using the `-test.v` flag to show the log I have)

```
$ go test golden_test.go -test.v -update
=== RUN   TestWrite
    golden_test.go:32: Wrote: testdata/TestWrite.golden.txt
--- PASS: TestWrite (0.00s)
PASS
ok  	command-line-arguments	0.090s
```

Then manually inspect it to ensure the function is correct:

```
$ cat testdata/TestWrite.golden.txt
hola
```

Then run the test again to see it pass:

```
$ go test golden_test.go
ok  	command-line-arguments	0.096s
```

## Code examples

Code examples can be added to tests and also show up in the docs! See [the Go blog](https://go.dev/blog/examples) for more details, or see my example below:

```
package main_test

import "fmt"

func ExampleExample() {
	fmt.Println("hello!")
	// Output: hello!
}
```
