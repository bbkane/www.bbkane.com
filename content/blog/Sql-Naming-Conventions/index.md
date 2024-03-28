+++
title = "SQL Naming Conventions"
date = 2024-03-27
+++

Let's have some fun writing some SQL naming conventions and applying them to [envelope](https://github.com/bbkane/envelope/)'s needs...

TODO: finish this... add envelope examples, add a summary of prefixes at the bottom

Some sources: 

- [Database, Table and Column Naming Conventions? - Stack Overflow](https://stackoverflow.com/questions/7662/database-table-and-column-naming-conventions)
- [A Quick Guide to Naming Conventions in SQL - Part 1](https://www.navicat.com/en/company/aboutus/blog/2132-a-quick-guide-to-naming-conventions-in-sql-part-1)
- [styleguide | Style guides for Google-originated open-source projects](https://google.github.io/styleguide/go/decisions#initialisms) - particularly around how to case `ID`.

# Tables

`PascalCase`, with the exception of joining tables which should be `TableOne_TableTwo `. 

Why? `snake_case` would have underscores in the table names, and I want to reserve those underscores for other things, like join tables, indexes, etc. No one seems to use `camelCase`, so I won't either. Also, `PascalCase` results in shorter names.

Tables should be a singular down, because pluralization is hard.

# Columns

`PascalCase`. Why? I don't really see the need to change it from table names and it maps closely to `sqlc` generated Go structs (which needs capitalized fields). If I get tired of using the shift key, I might change this to `camelCase`

Primary keys should be named `ID` . People advocate for naming it `TableNameID`, but I don't really think that's a big deal?

Foreign keys should be named `ReferencedTableNameID` . Foreign Key constraints shoudl be named `fk_ThisTable_ReferencedTable` (though I don't think this is applicable to SQLite).

# Indexes

# Views

# Triggers

