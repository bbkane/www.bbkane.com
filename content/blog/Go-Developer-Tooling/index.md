+++
title = "Go Developer Tooling"
date = 2023-02-18
updated = 2023-02-18
+++

My [Go repos](https://github.com/bbkane/) use several tools to make development
easier. I develop on a Mac, so install instructions are MacOS-focused.

See [example-go-cli](https://github.com/bbkane/example-go-cli) for a repo using these tools.

Also see [Go Project Notes](@/blog/Go-Project-Notes/index.md).

## [panicparse](https://github.com/maruel/panicparse)

Make panic stack traces much easier to read with colorization and removing extraneous info

![demo gif](https://raw.githubusercontent.com/wiki/maruel/panicparse/parse.gif)

### MacOS [Install](https://github.com/maruel/panicparse#installation)

```
go install github.com/maruel/panicparse/v2/cmd/pp@latest
```

### Run locally

```bash
go run . |& pp
```
