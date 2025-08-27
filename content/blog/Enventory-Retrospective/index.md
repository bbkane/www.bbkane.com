+++
title = "Enventory Retrospective"
date = 2025-08-26
draft = true
+++

# **enventory talk**

- Demo

  - Create env

  - Var ref

- Motivation

  - Fun

  - Learning

  - Solve a small problem I actually have

- Commit graph from observable
- Architecture
  - Layered- CLI, models, db

- CLI layer with warg

- Generate DB layer with sqlc

- Business layer in the middle

- LLMs and verbosity

- Transactions are messy, show article

- Observability 

  - Wrap the layers

  - OTEL

- Testing - snapshot tests. Requires determinism
- Packaging - goreleaser
- Dynamic tab completion with warg
- Expr to sort/filter
- Table output - too wide, switch to kvtable
- All writes from app, constraint enforcement from DB
  - Prevent same name with triggers

- Future plans

  - Env ref

  - Search?

- Other things to learn

  - Queues and other types of I/o (APIs, etc)

  - Auth

- Decorators for verbosity

