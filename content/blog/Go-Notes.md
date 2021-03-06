+++
title = "Go Notes"
date = 2018-09-04
updated = 2019-08-25
aliases = [ "2018/09/04/Go-Notes.html" ]
+++

These are things I want to remember in Go

## Format Strings

- `%+v` is introduced by Dave Cheney's [errors](https://github.com/pkg/errors) package. A common use case:

```go
if err != nil {
    // Add a stack
    err = errors.WithStack(err)
    log.Fatalf("%+v\n", err)
}
```

NOTE: I'm not sure this is the same as `panic(err)`. Something to check

- `%#v` is equivalent to Python's `repr` function - it formats the data structure like it would look if you typed it in code.

```go
s = NewMyStruct(param1, param2)
fmt.Printf("%#v\n", s)
```

## Using logrus

[logrus](https://github.com/sirupsen/logrus) is a pretty nice logging library for go. It focuses on logging key-value pairs along with a message. This is super useful for me because 90% of the time I just want to see those values anyway.

NOTE: I need to test this code

```go
package mypackage

import (
	log "github.com/sirupsen/logrus"
)

func myFunc() {
	log.WithFields(log.Fields{
		"sqlStatement": statement,
		"sqlArgs":      args,
	}).Debug("Oops")
}
```

```go
package main

import (
	log "github.com/sirupsen/logrus"
)

func init() {
	log.SetLevel(log.DebugLevel)
}

func main() {
	myFunc()
}
```


## Iterator type things in Go TODO

- PageDataIterator
- Scanner
- How to loop with it and for

