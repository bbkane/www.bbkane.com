+++
title = "Go Developer Tooling"
date = 2023-02-18
updated = 2023-02-18
+++

# Go Developer Tooling

My Go repos use several tools to make development easier. I develop on a Mac, so install instructions are MacOS-focused.

See [example-go-cli](https://github.com/bbkane/example-go-cli) for a repo using these tools.

## [golangci-lint](https://golangci-lint.run/)

Run various correctness checks on source code.

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

### MacOS Install

```bash
brew install goreleaser
```

### Run locally

```bash
goreleaser --snapshot --skip-publish --clean
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

## [VHS](https://github.com/charmbracelet/vhs)

Script demo GIF creation!

### MacOS Install

```bash
brew install vhs
```

### Run locally

```bash
vhs < demo.tape
```
