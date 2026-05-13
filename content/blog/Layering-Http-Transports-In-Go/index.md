+++
title = "Layering HTTP Transports in Go"
date = 2026-05-12
+++

Fairly recently, I worked on a project that makes a fair of different HTTP requests to different endpoints. This blog post covers techniques to make these HTTP requests easier and testable, in particular:

- Using the [earthboundkid/requests](https://github.com/earthboundkid/requests) library to make constructing the requests and getting the responses as easy as possible
- HTTP transports to add base configuration, testing, and other customization for HTTP requests.
- Retries with exponential backoff using [cenkalti/backoff](https://github.com/cenkalti/backoff)

# Easier requests with [earthboundkid/requests](https://github.com/earthboundkid/requests)

Standard Go wisdom is to NOT use a 3rd party library when Go's stdlib contains the needed functionality. Generally I agree with this, but I make an exception for `requests` because it's SO MUCH MORE ERGONOMIC than the stdlib and the core functionality of this app was to make HTTP requests. See [the README](https://github.com/earthboundkid/requests) and [wiki](https://github.com/earthboundkid/requests/wiki) for more details, 

TODO: example here; resume

# Transports

# Retrying requests with [cenkalti/backoff](https://github.com/cenkalti/backoff)

# Tying it all together

