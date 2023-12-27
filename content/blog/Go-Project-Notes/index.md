+++
title = "Go Project Notes"
date = 2023-12-27
aliases = [ "blog/go-notes/"]
+++

These are things I want to remember in Go. Also see [Go Developer Tooling](@/blog/Go-Developer-Tooling/index.md). and [Go Code Notes](@/blog/Go-Code-Notes/index.md).

 # Motivation

Simon Willison has a lot of projects - more than 100 of them I think. To manage them, he uses some custom tooling, custom libraries, and  a maintenance strategy he calls "[the perfect commit](https://simonwillison.net/2022/Jan/12/how-i-build-a-feature/)"  - each commit contains code changes, docs, and tests.

I don't have Simon's number of side projects, but I DO have a wife and toddler and I'm not as smart as him anyway. I've started adopting similar techniques (though using Go, not Python) to keep my side projects maintainable and fun during my limited time and energy to hack on them.

See [Checklists and Sayings](@/blog/Checklists-And-Sayings/index.md) for more exposition on codebases in general. Below are some notes for more Go-specific tools and workflows on projects.

# Creating a new Go project

Before starting, ask these questions:

- Will I use this or will I learn a lot from it?
- Is Go the right language? For small stuff Python works great!

Steps to take for new projects. I could use [cookiecutter](https://github.com/cookiecutter/cookiecutter) or similar tools to make this faster, but I find maintaining cookiecutter code difficult, so (right now) I prefer to manully copy example-go-cli and update the right thing by hand.

- Copy [example-go-cli](https://github.com/bbkane/example-go-cli)
- Erase the git history
- Commit
- Replace all references to it with the new name
- Update README
- Create repo on GitHub and push the code.
- Add the `go` topic to the repo
- Update [go.bbkane.com](https://github.com/bbkane/go.bbkane.com)
- Update CHANGELOG.md
- Add feature
- update demo.tape and update demo.gif with [vhs](https://github.com/charmbracelet/vhs) (`vhs < ./demo.tape`)
- Update [bbkane/bbkane](https://github.com/bbkane/bbkane).

If a the project is a CLI, not a library: 

- `go install go.bbkane.com/cli@latest` to test
- Add `KEY_GITHUB_GORELEASER_TO_HOMEBREW_TAP` to GitHub repo secrets
- Push a tag to build with `git tagit`
- `brew install bbkane/tap/cli`

If the project is a library, not a CLI:

- Delete the `.goreleasor.yml` file

# Code changes across Go repos

I occasionally need to update something across all the [Go projects](https://github.com/search?q=owner%3Abbkane+topic%3Ago&type=repositories) I maintain. I track most of these in my [Go Project Update Tracker Spreadsheet](https://docs.google.com/spreadsheets/d/1R0c6VFFU_vLC45zgs_53rcWDHWRxt4S6UxdxBkFgPpo/edit#gid=0), because the grid format makes it easy to see which changes are applied to which projects.

## Dependency updates

Once a project has enough tests for my satisfaction, let [Dependabot](https://docs.github.com/en/code-security/dependabot) make PRs with dependency updates.

## Easily automated changes

For example: a change to`.gitignore`, `.golangci.yml`, `.goreleaser.yml`, etc. that can be scripted with a shell script and/or [`yq`](https://github.com/mikefarah/yq)

I'm using [git-xargs-tasks](https://github.com/bbkane/git-xargs-tasks) to automate running the shell script against all my repos with [git-xargs](https://github.com/gruntwork-io/git-xargs). I recently used this to add YAML linting to all the YAML files I'm using in each repo (sorted keys, comment formatting, etc.).

## Changes that must be done manually

For example: a backwards incompatible `warg` update that requires callers to update:

- update [Go Project Update Tracker Spreadsheet](https://docs.google.com/spreadsheets/d/1R0c6VFFU_vLC45zgs_53rcWDHWRxt4S6UxdxBkFgPpo/edit#gid=0)
- update [example-go-cli](https://github.com/bbkane/example-go-cli) with the change and test. Update the CHANGELOG.md
- write a detailed issue that describes how to do the change
- add that issue to all repos (perhaps with a label)
- make the change to different projects as I get time/motivation and close the issue. Maybe before I add a feature to a project I close the change issue or before I start another manual change.

# Quality / Release tooling

- Must have:
  - Easy installation:
    - from editor
    - from CLI / pre-commit (via [lefthook](https://github.com/evilmartians/lefthook))
    - on GitHub Actions

- Should have:
  - Automatic fixes
  - Quick runtime


See `example-go-cli` [GitHub Action files](https://github.com/bbkane/example-go-cli/tree/master/.github/workflows) to see how I run these tools in CI

| Tool                                                         | MacOS Local Install          | Editor Integration                                           | CLI command                             | Automatic Fix                          |
| ------------------------------------------------------------ | ---------------------------- | ------------------------------------------------------------ | --------------------------------------- | -------------------------------------- |
| [`golang-ci-lint`](https://github.com/golangci/golangci-lint) | `brew install golangci-lint` | [VS Code](https://golangci-lint.run/usage/integrations/#go-for-visual-studio-code) | `golangci-lint run`                     | `golangci-lint run --fix`              |
| `go test`                                                    | `brew install go`            | [VS Code Testing tab](https://code.visualstudio.com/docs/languages/go#_test) | `go test`                               |                                        |
| [`yamllint`](https://github.com/adrienverge/yamllint)        | `brew install yamllint`      |                                                              | `yamllint .`                            | `yq -i -P 'sort_keys(..)' [file].yaml` |
| [`goreleaser`](https://github.com/goreleaser/goreleaser)     | `brew install goreleaser`    |                                                              | `goreleaser release --snapshot --clean` |                                        |

