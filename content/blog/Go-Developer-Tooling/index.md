+++
title = "Go Developer Tooling"
date = 2023-02-18
updated = 2023-02-18
+++

My [Go repos](https://github.com/bbkane/) use several tools to make development
easier. I develop on a Mac, so install instructions are MacOS-focused.

See [example-go-cli](https://github.com/bbkane/example-go-cli) for a repo using these tools.

Also see [Go Project Notes](@/blog/Go-Project-Notes/index.md).

## [golangci-lint](https://golangci-lint.run/)

Run various correctness checks on source code.

![demo gif](https://golangci-lint.run/demo.svg)

### MacOS [Install](https://golangci-lint.run/usage/install/#macos)

```bash
brew install golangci-lint
```

### Run [locally](https://golangci-lint.run/usage/quick-start/)
```bash
golangci-lint run
```

Note that with the `lintTool` set to `golangci-lint`, the `Go` VS Code extension will `go install` golangci-lint, despite the fact that this is [explicitly recommended against](https://golangci-lint.run/usage/install/#install-from-source). ¯\_(ツ)_/¯

## [GoReleaser](https://goreleaser.com/)

Build platform-specific executables and auto-update Homebrew taps and Scoop buckets.

![demo gif](https://raw.githubusercontent.com/goreleaser/example-simple/main/goreleaser.gif)

### MacOS Install

```bash
brew install goreleaser
```

### Run locally

```bash
goreleaser --snapshot --skip-publish --clean
```

## [gotestsum](https://github.com/gotestyourself/gotestsum)

Run Go tests with easier to read output, including color.

![example gif](https://user-images.githubusercontent.com/442180/182284939-e08a0aa5-4504-4e30-9e88-207ef47f4537.gif)

### MacOS [Install](https://github.com/gotestyourself/gotestsum)

```bash
go install gotest.tools/gotestsum@latest
```

### Run locally

```
gotestsum ./...
```

## [Lefthook](https://github.com/evilmartians/lefthook)

Install/Run/Uninstall pre-commit hooks that mimic CI.

### MacOS Install

```bash
brew install lefthook
```

Then run this from repo-root

```bash
lefthook install
```

### Run locally

- install pre-commit hook: `lefthook install`
- uninstall pre-commit hook: `lefthook uninstall`
- Run pre-commit without committing: `lefthook run pre-commit`

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

## [VHS](https://github.com/charmbracelet/vhs)

Script demo GIF creation!

![demo gif](https://camo.githubusercontent.com/1f2b0c758369c054538b7881b5d700739f2c37d2201f60ea26ad9311a7f88487/68747470733a2f2f73747566662e636861726d2e73682f7668732f6578616d706c65732f6e656f66657463685f332e676966)

### MacOS Install

```bash
brew install vhs
```

### Run locally

```bash
vhs < demo.tape
```
