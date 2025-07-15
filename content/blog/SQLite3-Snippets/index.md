+++
title = "SQLite3 Snippets"
date = 2016-07-11
updated = 2020-05-02
aliases = [ "2016/07/11/SQLite3-Snippets.html" ]
+++

Also see my related posts, [LinkedIn Recruiters Over Time](https://www.bbkane.com/blog/linkedin-recruiters-over-time/) and [Learn SQL](https://www.bbkane.com/blog/learn-sql/)

## Clients

The default `sqlite3` shell works ok, especially if it's [customized](https://github.com/bbkane/dotfiles/tree/master/sqlite3).

[litecli](https://litecli.com/) works well too - here's my [config](https://github.com/bbkane/dotfiles/tree/master/litecli).

[Beekeeper Studio](https://www.beekeeperstudio.io/), [Table Plus](https://tableplus.com/), and [DbGate](https://dbgate.org/) are all very decent GUI SQL clients.

## Creating a table

For some reason, the syntax doesn't seem to stick for me :)

This uses [strict tables](https://www.sqlite.org/stricttables.html)

```sql
DROP TABLE my_table;

CREATE TABLE my_table
(
    my_variable INTEGER NOT NULL PRIMARY KEY,
    my_other TEXT
) STRICT ;

INSERT INTO my_table VALUES (1, 'one');
INSERT INTO my_table VALUES (2, 'two');

SELECT * FROM my_table;
```

## Find duplicate columns in a table

I want to write somewhere an easy inner join to find records with duplicate
columns.

```sql
SELECT mt1.name
FROM
    my_table AS mt1
    JOIN my_table as mt2 ON mt1.name = mt2.name AND mt1.id != mt2.id
```

## See table structure

From [StackOverflow](https://stackoverflow.com/a/7679086/2958070):

```
PRAGMA table_info([tablename]);
```

## Find parents

See [StackOverflow](https://stackoverflow.com/a/68020920/2958070)

## SQL <3 CSV

Sqlite is great for crunching CSV files.

Here's a sample script:

Run the script with: `sqlite3 :memory: '.read script.sql'`

```sql
-- if a file doesn't have a header row, create a table for it
CREATE TABLE csv_subject ( col1 TEXT, col2 TEXT );

-- if you didn't create a table, the first row will be used
-- for column names
.import --csv filename.csv csv_subject

SELECT * FROM csv_subject LIMIT 10;

-- maybe manipulate a date or something
ALTER TABLE csv_subject ADD COLUMN sqlite_date TEXT;
UPDATE csv_subject SET sqlite_date = SUBSTR([col1], 0, 20);

-- can also use tsv
.mode csv
-- send the next query to a file
.once output.csv

SELECT * FROM csv_subject;
```

## Advanced SQL

See [this talk](https://youtu.be/xEDZQtAHpX8?t=1660) (the timestamp is to a very useful slide on `OVER`), and the associated [website](https://modern-sql.com/).

## SQLite3 Links

- [https://kerkour.com/sqlite-for-servers](Optimizing SQLite for servers) has some great tips.
