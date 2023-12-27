+++
title = "Go Project Notes"
date = 2023-12-27
aliases = [ "blog/go-notes/"]
+++

These are things I want to remember in Go. Also see [Go Developer Tooling](@/blog/Go-Developer-Tooling/index.md). and [Go Code Notes](@/blog/Go-Code-Notes/index.md)

 # Motivation

Simon Willison has a lot of projects - more than 100 of them I think. To manage them, he uses some custom tooling, custom libraries, and  a maintenance strategy he calls "https://simonwillison.net/2022/Jan/12/how-i-build-a-feature/"  - each commit contains code changes, docs, and tests.

I don't have Simon's number of side projects, but I DO have a wife and toddler and I'm not as smart as him anyway. I've started adopting similar techniques (though using Go, not Python) to keep my side projects maintainable and fun during my limited opportunities to hack on them.

See [Checklists and Sayings](@/blog/Checklists-And-Sayings/index.md) for more exposition on this in general. Below are some notes for more Go-specific tools and workflows on projects.

# Creating a new Go project

Before starting, ask these questions:

- Will I use this or will I learn a lot from it?
- Is Go the right language? For small stuff Python works great!

Steps to take for new projects. I could use https://github.com/cookiecutter/cookiecutter or something to make this faster, but I find maintaining cookiecutter code difficult, so I prefer to manully copy example-go-cli and update the right thing by hand. I'll probably write a script to do this at some point.

- Copy [example-go-cli](https://github.com/bbkane/example-go-cli)
- Erase the git history
- Commit
- Replace all references to it with the new name
- Update README
- Create repo on GitHub and push the code.
- Add the `go` topic to the repo
- Update [go.bbkane.com](https://github.com/bbkane/go.bbkane.com)
- Update CHANGELOG - TODO: ensure go-example-cli has a changelog
- Add feature
- update demo.tape and update demo.gif with vhs TODO link (`vhs < ./demo.tape`)
- Update [bbkane/bbkane](https://github.com/bbkane/bbkane).

If a the project is a CLI, not a library: 

- `go install go.bbkane.com/cli@latest` to test
- Add `KEY_GITHUB_GORELEASER_TO_HOMEBREW_TAP` to GitHub repo secrets
- Push a tag to build with `git tagit`
- `brew install bbkane/tap/cli`

If the project is a library, not a CLI:

- Delete the `.goreleasor.yml` file

# Code changes across Go repos

I occasionally need to update something across all the [Go projects](https://github.com/search?q=owner%3Abbkane+topic%3Ago&type=repositories) I maintain. I track most of these in [Go Project Update Tracker Spreadsheet](https://docs.google.com/spreadsheets/d/1R0c6VFFU_vLC45zgs_53rcWDHWRxt4S6UxdxBkFgPpo/edit#gid=0), because the grid format makes it easy to see which changes are applied to which projects.

## Dependency updates

Once a project has enough tests for my satisfaction, use GitHub's Dependabot

## Easily automated changes

For example: a change to`.gitignore`, `.golangci.yml`, `.goreleaser.yml`, etc. that can be scripted with a shell script and/or `yq`  TODO link.

I'm using [git-xargs-tasks](https://github.com/bbkane/git-xargs-tasks) to automate running the shell script against all my repos with [git-xargs](https://github.com/gruntwork-io/git-xargs). I recently used this to add YAML linting to all the YAML files I'm using in each repo (sorted keys, comment formatting, etc.).

## Changes that must be done manually

For example: a backwards incompatible `warg` update that requires callers to update:

- update [Go Project Update Tracker Spreadsheet](https://docs.google.com/spreadsheets/d/1R0c6VFFU_vLC45zgs_53rcWDHWRxt4S6UxdxBkFgPpo/edit#gid=0)
- update [example-go-cli](https://github.com/bbkane/example-go-cli) with the change and test
- write a detailed issue that describes how to do the change
- add that issue to all repos (perhaps with a label)
- make the change to different projects as I get time/motivation and close the issue. Maybe before I add a feature to a project I close the change issue or before I start another manual change.

# Quality / Release tooling

- Must have:
  - easily install and run:
    - from editor
    - from CLI / pre-commit (via lefthook TODO link)
    - on GitHub Actions

- Should have:
  - Automatic fixes
  - Quick runtime


See example-go-cli TODO link GitHub Action files for current implementation there

| Tool - TODO link | MacOS Local Install  | Editor Integration         | CLI command                             | Automatic Fix                          |
| ---------------- | -------------------- | -------------------------- | --------------------------------------- | -------------------------------------- |
| `golang-ci-lint` | Homebrew             | VS Code - TODO get setting | `golangci-lint run`                     | `golangci-lint run --fix`              |
| `go test`        | Homebrew (with `go`) | VS Code Testing tab        | `go test`                               | None                                   |
| `yamllint`       | Homebrew             | None                       | `yamllint .`                            | `yq -i -P 'sort_keys(..)' [file].yaml` |
| `goreleaser`     | Homebrew             | None                       | `goreleaser release --snapshot --clean` | None                                   |

# Other Tooling

TODO panicparse and gotestsum
