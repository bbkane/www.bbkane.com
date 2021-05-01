.import --csv messages.csv messages

-- off timezones so SQLite understands the dates
ALTER TABLE messages ADD COLUMN sqlite_date TEXT;
UPDATE messages SET sqlite_date = SUBSTR([DATE], 0, 20);

.mode tabs
.once aggregated_reachouts.tsv
SELECT
    MIN(sqlite_date) AS reachout_date,
    ROW_NUMBER() OVER (ORDER BY sqlite_date) AS cumulative_count
FROM
    messages
GROUP BY [FROM]
ORDER BY sqlite_date ASC;
