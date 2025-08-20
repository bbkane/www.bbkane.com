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
