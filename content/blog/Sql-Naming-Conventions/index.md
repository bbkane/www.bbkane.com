+++
title = "SQL Naming Conventions"
date = 2024-03-27

+++

Let's have some fun writing some SQL naming conventions/standards so I can keep [envelope](https://github.com/bbkane/envelope/)'s database sane. I feel like I might be over-engineering by creating my own, yet another, SQL naming standard, but I'm having fun so here we go.

![xkcd standards](https://imgs.xkcd.com/comics/standards.png)

Some sources: 

- [Database, Table and Column Naming Conventions? - Stack Overflow](https://stackoverflow.com/questions/7662/database-table-and-column-naming-conventions)
- [styleguide | Style guides for Google-originated open-source projects](https://google.github.io/styleguide/go/decisions#initialisms) - borrowing stuff from Go's style guide too, particularly around how to case `ID`.
- [SQL Server Naming Standards - SQL_server_standards.pdf](https://www.isbe.net/Documents/SQL_server_standards.pdf) - I'm taking heavy inspiration from this. The main thing I'm changing is the prefix notation

TL;DR prefix table:

All prefixes are two letters

| prefix | notes        | Example                         |
| ------ | ------------ | ------------------------------- |
| `ix_`  | Index        | `ix_Var_EnvID`                  |
| `ux_`  | Unique Index | `ux_Var_EnvID_Name`             |
| `vw_`  | View         | `vw_Env_Var_Ref`                |
| `tr_`  | Trigger      | `tr_Var_Insert_CheckUniqueName` |

# Tables

`PascalCase`, including joining tables which should be `TableOneTableTwo`. 

Why? `snake_case` would have underscores in the table names, and I want to reserve those underscores for other things, like join tables, indexes, etc. No one seems to use `camelCase`, so I won't either. Also, `PascalCase` results in shorter names.

Tables should be a singular down, because pluralization is hard.

Examples from envelope:

- `Env`
- `Var`
- `Ref`
- `KeyringEntry`
- `EnvChildUniqueName`

# Columns

`PascalCase`. Why? I don't really see the need to change it from table names and it maps closely to `sqlc` generated Go structs (which needs capitalized fields). If I get tired of using the shift key, I might change this to `camelCase`

Primary keys should be prefixed with the table name: `TableNameID` . This is a little inconsistent with other columns in the table (I don't advise prefixing them with the table name), and it feels less "DRY" when working with just one table, but is helpful for the following:

- foreign key columns can be named the same as the primary keys they're pointing to
- when doing adhoc queries using joins, it's nice to be able to use `SELECT *` and not have to use an `AS` clause to rename the ID fields from multiple tables.
- It maps nicely to the [New Type Idiom](https://doc.rust-lang.org/rust-by-example/generics/new_types.html) in calling code.

Foreign keys should be named `ReferencedTableNameID` . If there is already a foreign key with the same name, or it's pointing to the primary key, prefix it with a descriptive adjective : `ParentOrderID` .

Envelope example:

```sql
CREATE TABLE Var (
    VarID INTEGER PRIMARY KEY,
    EnvID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    Comment TEXT NOT NULL,
    CreateTime TEXT NOT NULL,
    UpdateTime TEXT NOT NULL,
    Value TEXT NOT NULL,
    FOREIGN KEY (EnvID) REFERENCES Env(EnvID) ON DELETE CASCADE,
    UNIQUE(EnvID, Name)
) STRICT;
```

# Indexes

Non Indexes should be prefixed with `ix`. Unique indexes should be prefixed with `ux`. Then add the table name and the purpose, separated by underscores. Sometimes the purpose is just the column name(s).

Envelope example:

- `ix_Var_EnvID` - create index on `EnvID` to [speed up foreign key checks](https://www.sqlite.org/foreignkeys.html#fk_indexes)
- `ux_Var_EnvID_Name` - unique constraint on the EnvID and Name fields (envelope uses this to help ensure we don't end up with env vars with duplicate names).

# Views

View should be prefixed with `vw_` . 

Why? Lightly edited quote from [SQL Server Naming Standards - SQL_server_standards.pdf](https://www.isbe.net/Documents/SQL_server_standards.pdf):

> Rule 5b (View Types) - Some views are simply tabular
> representations of one or more tables with a filter applied or because
> of security procedures (users given permissions on views instead of
> the underlying table(s) in some cases). Some views are used to
> generate report data with more specific values in the WHERE clause.
> Naming your views should be different depending on the type or
> purpose of the view. For simple views that just join one or more tables
> with no selection criteria, combine the names of the tables joined. For
> example, joining the "Customer" and "StateAndProvince" table to
> create a view of Customers and their respective geographical data
> should be given a name like "vw_CustomerStateAndProvince". Views
> created expressly for a report should have an additional prefix of
> Report applied to them, e.g. vw_ReportDivisionSalesFor2008.

Envelope example:

- `vw_Env_Var` - get the name of the environment and the name of the variable in a view instead of always having to join the tables.
- `vw_Env_Var_Ref` - same thing, but for references.

# Triggers

https://stackoverflow.com/a/32987440/2958070 - TODO for envelope

Lightly edited from [SQL Server Naming Standards - SQL_server_standards.pdf](https://www.isbe.net/Documents/SQL_server_standards.pdf):

> Triggers have many things in common with stored procedures.
> However, triggers are different than stored procedures in two
> important ways. First, triggers don't exist on their own. They are
> dependent upon a table. So it is wise to include the name of this table
> in the trigger name. Second, triggers can only execute when an Insert,
> Update, or Delete happens on one or more of the records in the table.
> So it also makes sense to include the type of action that will cause the
> trigger to execute.

I'm going to try to use name my triggers like `tr_{TableName}_{Insert|Update|Delete}_{reason}` and see how that works out.

Envelope example:

- `tr_Var_Insert_CheckUniqueName`

