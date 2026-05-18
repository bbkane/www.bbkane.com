+++
title = "HTTP Client Tricks in Go"
date = 2026-05-12
+++

Fairly recently, I worked on a project that makes a fair amount of different HTTP requests to different endpoints. This blog post covers techniques to make these HTTP requests easier and testable, in particular:

- Using the [earthboundkid/requests](https://github.com/earthboundkid/requests) library to make constructing the requests and getting the responses as easy and error-free as possible
- HTTP RoundTrippers to add base configuration, testing, and other customization for HTTP requests.
- Retries with exponential backoff using [cenkalti/backoff](https://github.com/cenkalti/backoff)

# Ergonomic requests with [earthboundkid/requests](https://github.com/earthboundkid/requests)

Standard Go wisdom is to NOT use a 3rd party library when Go's stdlib contains the needed functionality. Generally I agree with this, but I make an exception for `requests` because it's SO MUCH MORE ERGONOMIC than the stdlib and the core functionality of this app was to make HTTP requests. See [the README](https://github.com/earthboundkid/requests) and [wiki](https://github.com/earthboundkid/requests/wiki) for more details, but here's an example:

```go
req := requests.
  URL(baseURL).
  Path("/somePath").
  BodyJSON(&payload).
  Method(http.MethodPost).
  ContentType("application/json").
  Accept("application/json").
  Header("Connection", "keep-alive").
  Param("start", start).
  Param("end", end).
  ToJSON(&response).
  Client(&c.client).
  AddValidator(WrapRetriableStatuses)
```

This would be.. a lot harder to write, read, and keep error free with `net/http`'s interface.

# [`http.RoundTripper`](https://pkg.go.dev/net/http#RoundTripper) Refresher

the `http.RoundTripper` interface is the primary way Go allows devs to modify HTTP requests:

```go
type RoundTripper interface {
  // snip: doc comments (see the link above)
	RoundTrip(*Request) (*Response, error)
}
```

The default `http.Client` implements `RoundTripper`, and by default code just uses that. However, you can **nest** these to modify requests before they're sent and responses after they arrive.

![image-20260513055629994](index.assets/image-20260513055629994.png)

These things can be nested without limit as long as each `RoundTripper`'s implementation allows an innter `RoundTripper` to delegate to. 

For example, the [`golang.org/x/oauth2`](https://pkg.go.dev/golang.org/x/oauth2) package [provides](https://pkg.go.dev/golang.org/x/oauth2#Transport) a `RoundTripper` that can be used on top of another `RoundTripper` (the default `http.Client` is a good option) to allow oath authentication.

Also, a note on terminology:  `http.RoundTripper` is an **interface** defining how a request is executed, while `http.Transport` is a concrete **struct** that implements that interface with low-level network capabilities. I find it a bit confusing because the `http.Client` struct has a field called `Transport` that has type `http.RoundTripper` (why didn't they call that field `RoundTripper`?). In any case I'll use the terms `RoundTripper` and `Transport` interchangeably.

# Common settings in a "base" `RoundTripper`

For production, this is the innermost `RoundTripper` that actually makes the HTTP requests. Example (Claude-generated, for inspiration). This is where common settings should go: timeouts, proxy settings, observability...

```go
 import (
"net"
"net/http"
"time"
)

func NewBaseTransport() http.RoundTripper {
	t := http.DefaultTransport.(*http.Transport).Clone()
	t.MaxIdleConnsPerHost = 10
	return t
}
```

# Snapshot Tests

The goal of snapshot tests are to easily get realistic HTTP responses for testing purposes. This is done by recording a "snapshot" of a *live* HTTP response to disk when an environment variable is set. In "replay" mode, when the environment variable is NOT set, the test uses the recorded snapshot for its purposes.

The upside is that you don't have to mock data, you can simply use the recorded live data. The downside is that you can't easily get the exact data you want (it's recorded live), so you have to keep your test asserts fairly general and use other code to test rarer error conditions you can't easily trigger live.

Fortunately, [earthboundkid/requests](https://github.com/earthboundkid/requests) has a `reqtest` package with a transport that does the actual recording work. We simply have to compose transports:

- the record or replay transport as the "outermost" one
- one "auth" transport just for this HTTP request. We need to set auth in this transport instead of in the `requests` call to ensure the auth header isn't recorded.
- one "base" transport to with common settings for all HTTP requests (see above)

## `main.go`

```go
// main.go

package main

import (
	"context"
	"fmt"
	"net/http"
	"regexp"

	"github.com/carlmjohnson/requests"
)

// transport for all HTTP requests. Sets common settings
func NewBaseTransport() http.RoundTripper {
	t := http.DefaultTransport.(*http.Transport).Clone()
	t.MaxIdleConnsPerHost = 10
	return t
}

// Transport that adds auth header just for some requests. Wraps another transport to do the actual work.
// NOTE that we need to add auth in the transport instead of the `requests` call to hide it from `reqtest` and avoid it being recorded in snapshots.
func AddAuth(transport http.RoundTripper) http.RoundTripper {
	return requests.RoundTripFunc(func(req *http.Request) (*http.Response, error) {
		req2 := *req
		req2.Header.Set("Authorization", "Bearer mytoken")
		return transport.RoundTrip(&req2)
	})
}

// FetchTitle GETs example.com and returns the contents of its <title> tag.
// The transport is passed in so tests can inject record/replay.
func FetchTitle(ctx context.Context, transport http.RoundTripper) (string, error) {
	var body string
	err := requests.
		URL("https://example.com").
		Transport(transport).
		ToString(&body).
		Fetch(ctx)
	if err != nil {
		return "", fmt.Errorf("fetching example.com: %w", err)
	}

	m := regexp.MustCompile(`<title>([^<]+)</title>`).FindStringSubmatch(body)
	if m == nil {
		return "", fmt.Errorf("no <title> in response")
	}
	return m[1], nil
}

func main() {
	ctx := context.Background()
	transport := NewBaseTransport()
	transport = AddAuth(transport)
	title, err := FetchTitle(ctx, transport)
	if err != nil {
		panic(err)
	}
	fmt.Println(title)
}

```

## `main_test.go`

```go
package main

import (
	"context"
	"net/http"
	"os"
	"path/filepath"
	"testing"

	"github.com/carlmjohnson/requests/reqtest"
	"github.com/stretchr/testify/require"
)

func TestFetchTitle(t *testing.T) {
	require := require.New(t)
	ctx := context.Background()

	updateSnapshot := os.Getenv("UPDATE_SNAPSHOTS") != ""
	snapshotDir := filepath.Join("testdata", t.Name())

	var transport http.RoundTripper

	if updateSnapshot {
		// delete previous snapshots and remake dir
		err := os.RemoveAll(snapshotDir)
		require.NoError(err)
		err = os.MkdirAll(snapshotDir, 0700)
		require.NoError(err)

		// Record mode: hit example.com with the same transport the app uses
		// and write the request/response pair to disk under snapshotDir.
		transport = NewBaseTransport()
		transport = AddAuth(transport)
		transport = reqtest.Record(transport, snapshotDir)
	} else {
		// Replay mode (the default): serve responses from disk.
		// Never touches the network — the test is hermetic.
		transport = reqtest.Replay(snapshotDir)
	}

	title, err := FetchTitle(ctx, transport)
	require.NoError(err)
	require.Equal("Example Domain", title)
}

```

# Retrying requests with [cenkalti/backoff](https://github.com/cenkalti/backoff)

HTTP Requests also ([sometimes](https://www.youtube.com/watch?v=rvHd4Y76-fs)) need to be retried if they fail. [cenkalti/backoff](https://github.com/cenkalti/backoff) is a decent library to do that, and here's how you can use it with `requests`

## `retry.go`

```go
package main

import (
	"context"
	"fmt"
	"math"
	"net/http"
	"strconv"
	"time"

	"github.com/cenkalti/backoff/v5"
)

// WrapRetriableStatuses converts HTTP responses into errors that can be retried with backoff.Retry (or not retried).
// Used as a validator for requests
func WrapRetriableStatuses(resp *http.Response) error {
	switch {
	// 2xx are successful responses, so no error
	case resp.StatusCode >= 200 && resp.StatusCode <= 299:
		return nil

	// http.StatusTooManyRequests says how long to wait before retry
	case resp.StatusCode == http.StatusTooManyRequests:
		seconds, err := strconv.ParseInt(resp.Header.Get("Retry-After"), 10, 64)
		if err == nil && seconds >= 0 && seconds <= math.MaxInt32 {
			return backoff.RetryAfter(int(seconds))
		}
		return fmt.Errorf("retry after: %d", seconds)

	// treat 5xx as retriable errors
	case resp.StatusCode >= 500 && resp.StatusCode <= 599:
		return fmt.Errorf("retry on 5xx: %d", resp.StatusCode)

	// don't retry on any other errors
	default:
		return backoff.Permanent(fmt.Errorf("non-retriable error: status code %d", resp.StatusCode))
	}
}

func Retry(ctx context.Context, f func() error) error {
	// adapt to the signature that backoff.Retry expects
	action := func() (struct{}, error) {
		err := f()
		return struct{}{}, err
	}
	_, err := backoff.Retry(
		ctx,
		action,
		backoff.WithBackOff(&backoff.ExponentialBackOff{
			// these settings are just for demo purposes, not necessarily good defaults
			InitialInterval:     2 * time.Second,
			RandomizationFactor: 0.1,
			Multiplier:          1.5,
			MaxInterval:         15 * time.Second,
		}),
		backoff.WithMaxTries(3),
	)
	return err
}
```

## Update  `FetchTitle` with retries

```go
// FetchTitle GETs example.com and returns the contents of its <title> tag.
// The transport is passed in so tests can inject record/replay.
func FetchTitle(ctx context.Context, transport http.RoundTripper) (string, error) {
	var body string

	req := requests.
		URL("https://example.com").
		Transport(transport).
		ToString(&body).
		AddValidator(WrapRetriableStatuses)

	err := Retry(ctx, func() error {
		err := req.Fetch(ctx)
		if err != nil {
			slog.WarnContext(ctx, "FetchTitle error")
		}
		return err
	})

	if err != nil {
		return "", fmt.Errorf("error fetching example.com: %w", err)
	}

	m := regexp.MustCompile(`<title>([^<]+)</title>`).FindStringSubmatch(body)
	if m == nil {
		return "", fmt.Errorf("no <title> in response")
	}
	return m[1], nil
}
```



