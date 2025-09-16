+++
title = "SQL Isolation Levels"
date = 2025-08-19
draft = true
+++

These are some notes on SQL Isolation levels - what are they, what are some examples of what happens at different isolation levels; hopefully some diagrams

Links:

- https://www.pingcap.com/article/what-are-sql-isolation-levels-and-how-to-choose/
- https://www.youtube.com/watch?v=5ZjhNTM8XU8
- [Jepsen 15: What Even Are Transactions? by Kyle Kingsbury - YouTube](https://www.youtube.com/watch?v=ecZp6cWhDjg)
- [Jepsen 18: Serializable Mom by Kyle Kingsbury - YouTube](https://www.youtube.com/watch?v=dpTxWePmW5Y)

Things to define:

- what is Snapshot isolation?

# [Jepsen 15: What Even Are Transactions? by Kyle Kingsbury - YouTube](https://www.youtube.com/watch?v=ecZp6cWhDjg)

7m55 - Snapshot isolation ??

8m17s - Concurrent cluster-wide transations are guaranteed  to appear as if they are run one at at time (serializable isolation level)

# [@xyuanlu's Isolation Notes](https://github.com/xyuanlu/LosGatosSeminar/blob/main/basics/Isolation)

The concept of database isolation provides programmers with the illusion of a single-threaded environment. The isolation guarantee states that transactions are executed as if there are no concurrent transactions (when in fact there ARE)

## Concurrent write/read errors

- **dirty write** - write based on uncommitted value, and commit before previous uncommitted value commit (which could be rolled back)
- **dirty read** - read uncommitted data
- **non-repeatable read** - Reading a row twice in the same transaction results in different data
- **phantom read** - When a transaction re-executes a query, rows in the later query read are not in the first read (TODO: how is this different than the non-repeatable read)
- **write skew** - 2 transactions read the same set of data and update disjoint subsets. TODO: understand this example better

## Different isolation levels

- **Read Uncommitted** - can read aything
- **Read Committed** - can read any data that has been committted at the moment of reading (not necessarily the start of the transaction)
- **Repeatable Read** - All reads withing a transaction see the same data (TODO: how does this affect data written within the transaction?)
- **Serializable** - complete isolation: the final result must be equivalent to a result that would have occurred without concurrency.

|                  | Dirty Write  | Ditry Read   | Non-Repeatable Read | Phantom Read |
| ---------------- | ------------ | ------------ | ------------------- | ------------ |
| Read Uncommitted | Not Possible | Possible     | Possible            | Possible     |
| Read Committed   | Not Possible | Not Possible | Possible            | Possible     |
| Repeatable Read  | Not Possible | Not Possible | Not Possible        | Possible     |
| Serializable     | Not Possible | Not Possible | Not Possible        | Not Possible |

NOTE: the SQL Standard did not accurately define database isolation levels and different vendors attach liberal and non-standard semantics to name their own isolation levels (TODO: where are these definitions from?)

- Snapshot Isolation - guarantees that all reads made in a transaction will see a consistent snapshot of a database. In practice it reads the last comitted values that existed at the same time it strted. It won't have dirty read/write and guarantees repeatabl reads. However, depending on different vendors and their definitions, some implementations are also vulnerable to the phantom read anomaly. Snapshot isolation is also vulnerable to the write skew anamoloy

TODO: find jepson isolation definitions

TODO: rename this database semantics

Links: TODO: read

- https://en.wikipedia.org/wiki/Snapshot_isolation
- https://dbmsmusings.blogspot.com/2019/05/introduction-to-transaction-isolation.html
