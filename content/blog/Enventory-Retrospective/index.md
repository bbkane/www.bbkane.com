+++
title = "Enventory Retrospective"
date = 2025-08-26
draft = true
+++

I've had a lot of fun writing [enventory](https://github.com/bbkane/enventory), and here on some notes of what I've learned (mostly about architecture and Go)! I'm writing this post as an alternative to slides for a talk to give a few friends.

# What is enventory?

> Centrally manage environment variables with SQLite
>
> - Automatically export/unexport environments when entering/leaving directories
> - Keep a global view of which variables apply to which projects (as well as date created/updated, optional comments).
> - Filter environments to keep your view manageable:
>
> ```
> enventory env list --expr 'filter(Envs, hasPrefix(.Name, "test") and .UpdateTime > now() - duration("90d"))'
> ```
>
> - Share variables between environments with variable references
> - Advanced tab completion! Autocomplete commands, flags, env names, var/ref names
> - Currently only supports `zsh`

![demo.gif](https://raw.githubusercontent.com/bbkane/enventory/master/demo.gif)

# Motivation

- Solve a small problem I have 

- Learning
  - I've never been happy with CRUD architures in work projects
  - Take my time writing, learning, and rewriting my own CRUD architecture

- Fun! (and exercise [my CLI library](https://github.com/bbkane/warg))

# Commit Stats

~360 commits over 1.75 years

<img src="./index.assets/image-20251009212831560.png" alt="image-20251009212831560" style="zoom:60%;" />

Side project schedule: mornings, evenings, weekends

Most commits around 5PM Sundays 🤷‍♂️

![image-20251008215545080](./index.assets/image-20251008215545080.png)

~4500 lines of code

```
$ tokei --compact
===============================================================================
 Language            Files        Lines         Code     Comments       Blanks
===============================================================================
 Go                     32         5426         4577          168          681
 JSON                    1            1            1            0            0
 Markdown               12          707            0          455          252
 SQL                     9          458          349           41           68
 SVG                     8          711          658           53            0
 Plain Text            160          285            0          285            0
 YAML                    3           39           32            6            1
 Zsh                     2           95           64           13           18
===============================================================================
 Total                 227         7722         5681         1021         1020
===============================================================================
```

# Architecture

A "layered architecture" inspired by the [WTF Dial blog posts

![image-20250120202741319](./index.assets/image-20250120202741319.png)

This is viewable in the import graph:

- Top level "presentation" layer - `cli` package
- Business layer in the middle - `app` package
- Generate DB layer with [sqlc](https://sqlc.dev/) - `sqlcgen` package
- `cli` and `app` packages share types via a `models` package

# Layered Architecture Thoughts

Advantages:

- easy to add/enforce things within a layer (i.e., adding observability to a layer is as simple as wrapping the layer's interface with one that logged the method and called the layer )
- It's generally pretty easy to know where to put things (sometimes hard between CLI and business layer)

Disadvantages

- Lots of translating between the layers
- Adding a feature means updating all the layers
- Layers can get thick with lots of methods

Other:

- I tried to break this up even further (hexagonal architecture), but all my things refer to each other so I didn't find a good place.

# CLI Design Notes

- Make CLIs you'll actually use. You'll quickly discover what features they need
- Read a few CLI design guides and pick a favorite (like [this](https://m.youtube.com/watch?v=eMz0vni6PAw) (REALLY good Cobra talk) or [this](https://fuchsia.dev/fuchsia-src/development/api/cli#ux-guidelines) or [this](https://rust-cli-recommendations.sunshowers.io/index.html))
  - I picked the "subcommand subcommand verb flags" way inspired by [`azure-cli`](https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest)
- Iterate on your app's CLI design (any subcommands, flags, etc) in a text file before coding it up to make sure everything is nicely  organized

<img src="./index.assets/image-20251009215257929.png" alt="image-20251009215257929" style="zoom:50%;" />

# CLI Implementation

- 6 sections (used to group commands)
- 19 commands total (so far)

Command nesting is [pretty declarative](https://github.com/bbkane/enventory/blob/d8eb5315cb6784ed9473a77fd50633475f978787/main.go#L12):

```go
app := warg.New(
  "enventory",
  version,
  warg.NewSection(
    "Manage Environmental secrets centrally",
    warg.NewSubSection(
      "completion",
      "Print completion scripts",
      warg.SubCmd("zsh", cli.CompletionZshCmd()),
    ),
    warg.NewSubSection(
      "env",
      "Environment commands",
      warg.SubCmd("create", cli.EnvCreateCmd()),
      warg.SubCmd("delete", cli.EnvDeleteCmd()),
      warg.SubCmd("list", cli.EnvListCmd()),
      warg.SubCmd("update", cli.EnvUpdateCmd()),
      warg.SubCmd("show", cli.EnvShowCmd()),
    ),
    // more sections / commands
```

 Setting up a command is also not bad (using helper functions as some of these flags are re-used)

```go
func EnvDeleteCmd() warg.Cmd {
  return warg.NewCmd(
    "Delete an environment and associated vars",
    withConfirm(withSetup(envDelete)),
    warg.CmdFlag("--name", envNameFlag()),
    warg.CmdFlagMap(confirmFlag()),
    warg.CmdFlagMap(timeoutFlagMap()),
    warg.CmdFlagMap(sqliteDSNFlagMap()),
  )
}
```

Piping the parsed flags into the business layer is a bit annoying, as is dealing with errors:

```go
func envDelete(ctx context.Context, es models.Service, cmdCtx warg.CmdContext) error {
  name := mustGetNameArg(cmdCtx.Flags)
  err := es.WithTx(ctx, func(ctx context.Context, es models.Service) error {
    err := es.EnvDelete(ctx, name)
    if err != nil {
      return fmt.Errorf("could not delete env: %s: %w", name, err)
    }
    return nil
  })
  if err != nil {
    return err
  }

  fmt.Fprintf(cmdCtx.Stdout, "deleted: %s\n", name)
  return nil
}
```

Use decorators like `withSetup` or `withConfirm` to reduce verbosity:

```go
// withConfirm wraps a cli.Action to ask for confirmation before running
func withConfirm(f func(cmdCtx warg.CmdContext) error) warg.Action {
  return func(cmdCtx warg.CmdContext) error {
    confirm := cmdCtx.Flags["--confirm"].(bool)
    if !confirm {
      return f(cmdCtx)
    }

    fmt.Print("Type 'yes' to continue: ")
    reader := bufio.NewReader(os.Stdin)
    confirmation, err := reader.ReadString('\n')
    if err != nil {
      return fmt.Errorf("confirmation ReadString error: %w", err)
    }
    confirmation = strings.TrimSpace(confirmation)
    if confirmation != "yes" {
      return fmt.Errorf("unconfirmed change")
    }
    return f(cmdCtx)
  }
}

```

# CLI Snapshot Testing

Allow deterministic output with either flags or a special app setup, so you can easily write snapshot tests.

- [`enventory`](https://github.com/bbkane/enventory) has a `--create-time` flag that defaults to the current time but can be passed a date so the output is deterministic. 
- [`shovel`](https://github.com/bbkane/shovel) allows the app to be constructed with an [injectable I/O function](https://github.com/bbkane/shovel/blob/fb7e91479b15e58a14f8969ff9366942ecbdf3b8/dig/dig.go#L38). Tests use a mock function, `main()` uses a real one

Enventory is small and self-contained enough that snapshot tests are fast and convenient!

- Why test one layer when you can test them all at once?
- Each test makes its own SQLite DB
- Tests are run in parallel (enforced by [`paralleltest`](https://golangci-lint.run/docs/linters/configuration/#paralleltest))

# CLI Test Example

- Most tests are a [sequence of enventory commands](https://github.com/bbkane/enventory/blob/d8eb5315cb6784ed9473a77fd50633475f978787/main_env_test.go#L29) with a small "Builder" DSL to get easy tab completion

```go
tests := []testcase{
  {
    name:            "01_envCreate",
    args:            envCreateTestCmd(dbName, envName01),
    expectActionErr: false,
  },
  {
    name: "02_envShow",
    args: new(testCmdBuilder).Strs("env", "show").
      Name(envName01).Tz().Mask(false).Finish(dbName),
    expectActionErr: false,
  },
  {
    name: "03_envList",
    args: new(testCmdBuilder).Strs("env", "list").
      Strs("--timezone", "utc").Finish(dbName),
    expectActionErr: false,
  },
}

```

`stderr` and `stdout` are compared [against files](https://github.com/bbkane/enventory/tree/master/testdata) and and the test fails if the output doesn't match.

Example file content:

```
╭────────────┬────────────────╮
│ Name       │ envName01      │
│ CreateTime │ Mon 0001-01-01 │
╰────────────┴────────────────╯
```

# CLI Tab Completion

CLI commands that are painfully long to type

```bash
enventory var ref create \
    --env /path/to/project \
    --name example_com_API_KEY \
    --ref-env example_com_env \
    --ref-var example_com_API_KEY
```

Most of these can be tab completed! 

Added **REALLY GOOD** tab completion to autocomplete basically anything already in the database (i.e., `--env`, `--ref-env`, `--ref-var`), scoped by previous passed flags. Example: limits `--ref-var` suggestions to  variables that exist in `--ref-env`.

# App Layer

Implements interface from `models` package, handles transactions to database layer.

I couldn't figure out a meaningful way to isolate functionality, so it's one big interface...

```go
type Service interface {
  EnvCreate(ctx context.Context, args EnvCreateArgs) (*Env, error)
  EnvDelete(ctx context.Context, name string) error
  EnvList(ctx context.Context, args EnvListArgs) ([]Env, error)
  EnvUpdate(ctx context.Context, name string, args EnvUpdateArgs) error
  EnvShow(ctx context.Context, name string) (*Env, error)

  VarCreate(ctx context.Context, args VarCreateArgs) (*Var, error)
  VarDelete(ctx context.Context, envName string, name string) error
  VarList(ctx context.Context, envName string) ([]Var, error)
  VarUpdate(ctx context.Context, envName string, name string, args VarUpdateArgs) error
  VarShow(ctx context.Context, envName string, name string) (*Var, []VarRef, error)

  VarRefCreate(ctx context.Context, args VarRefCreateArgs) (*VarRef, error)
  VarRefDelete(ctx context.Context, envName string, name string) error
  VarRefList(ctx context.Context, envName string) ([]VarRef, []Var, error)
  VarRefShow(ctx context.Context, envName string, name string) (*VarRef, *Var, error)
  VarRefUpdate(ctx context.Context, envName string, name string, args VarRefUpdateArgs) error

  WithTx(ctx context.Context, fn func(ctx context.Context, es Service) error) error
}
```

# App Transactions

Allows callers to run arbitrary code in the callback `fn`. Try to keep transactions at the top level.

```go
WithTx(ctx context.Context, fn func(ctx context.Context, es Service) error) error
```

Inspiration: [Transactions in Go Hexagonal Architecture | by Khaled Karam | The Qonto Way | Medium](https://medium.com/qonto-way/transactions-in-go-hexagonal-architecture-f12c7a817a61)

Usage:

```go
err := es.WithTx(ctx, func(ctx context.Context, es models.Service) error {
  var err error
  env, err = es.EnvCreate(ctx, createArgs)
  if err != nil {
    return err
  }
  return nil
})
if err != nil {
  return fmt.Errorf("could not create env: %w", err)
}
```

# DB Layer

- Shove data into the database
- Simple dataflow model:
  - App layer does all writes
  - DB layer rejects writes that that violate constraints
- Migrate with SQL files
- Generate Go -> SQL functions with [sqlc.dev](https://sqlc.dev)
- Generate markdown docs with [k1LoW/tbls: tbls is a CI-Friendly tool to document a database, written in Go.](https://github.com/k1LoW/tbls)

# Main Tables



<img src="https://github.com/bbkane/enventory/raw/master/dbdoc/env.svg" alt="er" style="zoom:50%;" />

- All tables have `comment`, `create_time`, `update_time`
- Tables use `<tablename>_id` integer primary keys
  - Makes renames easy

# Cross-table UNIQUE Constraints

`var`s and `var ref`s are in different tables, yet must have unique names in the environment so exports work correctly.

Use views + triggers!

- Create a view with all the names in the env
- Use triggers to FAIL the insert/update if we can find the name in the view

```sqlite
CREATE TRIGGER tr_var_insert_check_unique_name
BEFORE INSERT ON var
FOR EACH ROW
BEGIN
SELECT RAISE(FAIL, 'name already exists in env')
FROM
vw_env_var_var_ref_unique_name
WHERE env_id = NEW.env_id AND name = NEW.name;
END
```

Thoughts

- I like that this is the "bottom layer" - upper layers don't need to validate this
- SQL is hard to write (limited autocomplete), debug and test

# SQL Migrations

- Plain SQL files - alter table, add tables, update views, etc.
- Embedded into the app binary
- Checked against migrations table on app startup to prevent running twice
- Migrations manually tested for now

```
sqlite> SELECT * FROM migration_v2;
┌─────────────────┬───────────────────────────────────────┬──────────────────────┐
│ migration_v2_id │               file_name               │     migrate_time     │
├─────────────────┼───────────────────────────────────────┼──────────────────────┤
│ 1               │ 001_create.sql                        │ 2024-09-04T04:04:33Z │
│ 2               │ 002_env_ref.sql                       │ 2024-09-04T04:04:33Z │
│ 3               │ 003_refactor.sql                      │ 2024-09-04T04:04:33Z │
│ 4               │ 004_allow_env_var_env_ref_updates.sql │ 2024-09-04T04:04:33Z │
│ 5               │ 005_drop_keyring_entry.sql            │ 2024-09-14T22:43:46Z │
│ 6               │ 006_var_and_ref_renames.sql           │ 2024-10-03T22:32:31Z │
└─────────────────┴───────────────────────────────────────┴──────────────────────┘
```

# Generate SQL -> Go

[`sqlc`](https://sqlc.dev) is amazing! It generates so much finicky boilerplate.

Write:

```sqlite
-- name: EnvCreate :one
INSERT INTO env (
    name, comment, create_time, update_time
) VALUES (
    ?   , ?      , ?          , ?
)
RETURNING name, comment, create_time, update_time;
```

Generate:

```go
func (q *Queries) EnvCreate(ctx context.Context, arg EnvCreateParams) (EnvCreateRow, error) {
  row := q.db.QueryRowContext(ctx, envCreate,
    arg.Name,
    arg.Comment,
    arg.CreateTime,
    arg.UpdateTime,
  )
  var i EnvCreateRow
  err := row.Scan(
    &i.Name,
    &i.Comment,
    &i.CreateTime,
    &i.UpdateTime,
  )
  return i, err
}
```

# Generate [SQL Docs](https://github.com/bbkane/enventory/tree/master/dbdoc) with [tbls](https://github.com/k1LoW/tbls)

![image-20251009223841419](./index.assets/image-20251009223841419.png)

# Outline

- LLMs and verbosity
- SQLC codegen + diagrams
- Observability 

  - Wrap the layers

  - OTEL
- Packaging - goreleaser
- Expr to sort/filter
- Table output - too wide, switch to kvtable
- Future plans

  - Env ref

  - Search?
  
  - backup on migration
- Other things to learn

  - Queues and other types of I/o (APIs, etc)

  - Auth
- Goreleaser
- Naming enventory
- zsh integration

