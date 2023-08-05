+++
title = "Monthly Banking Report"
date = 2023-08-01
+++

After [commenting on Hacker News](https://news.ycombinator.com/item?id=36987282), a few people asked me how I use [Polars](https://www.pola.rs/) to process my banking CSVs. While I don't feel comfortable open-sourcing the repo because the code contains information about the businesses I frequent to categorize the results, I can explain the data transformation pipeline between CSVs -> HTML report.

# Input Data

I download a checking activity CSV and a credit card activity CSV from my bank. I generally do this for the longest time window I can.

**export_20221225_chk.csv**

| Date       | Description                             | Comments | Check Number | Amount | Balance  |
| ---------- | --------------------------------------- | -------- | ------------ | ------ | -------- |
| 01/25/2021 | Purchase SQ *SALT & STRAW SAN JOSE CAUS |          |              | -$7.00 | $1234.56 |

**export_20221225_cc.csv**

| Transaction Date | Post Date  | Description                            | Category      | Trans. Amount |
| ---------------- | ---------- | -------------------------------------- | ------------- | ------------- |
| 12/18/2022       | 12/19/2022 | GOOGLE *YouTube Member g.co/helppay#CA | Digital Goods | $5.46         |

# Categorize

The next step is to add a category to each row in the checking CSV and to "clean up" categories in the credit card csv

For that, I use a function similar to the following:

```python
def add_checking_category(row: dict[str, str]) -> dict[str, str]:
    # Row is a dict containing the stuff from my bank CSV
    # "Date" TEXT,
    # "Description" TEXT,
    # "Comments" TEXT,
    # "Check Number" TEXT,
    # "Amount" TEXT,
    # "Balance" TEXT

    # Charitable Organizations
    if "something" in row["Description"]:
        row["category"] = "Destination Category"
    # .. more if/else statements
    # DEFAULT: Uncategorized
    else:
        row["category"] = "Uncategorized"
    return row
```

This approach is kind of brittle, but it *does* mean I don't need to pull machine learning or other more complicated techniques into my categorization.

I use a similar function to update the credit card categories (Note the dict at the bottom recategorizing categories I don't find useful, such as "Boating".

```python
def change_creditcard_category_row(row: dict[str, str]) -> dict[str, str]:
    # Row has these attributes:
    # "Transaction Date"
    # "Post Date"
    # "Description"
    # "Category"
    # "Trans. Amount"

    # Charitable Organizations
    if (
        "Charity name" in row["Description"]
        or "Alternate Charity Name" in row["Description"]
    ):
        row["Category"] = "Charitable Organizations"
        
    # ... more if/else statements

    # "bucket" categories
    new_categories = {
        "Airlines": "Travel - Other",
        "Apparel": "Retail",
        "Auto / Vehicle Rental": "Professional Services",
        "Boating": "Entertainment",
        # ... more category renames
    }

    row_category = row["Category"]
    if row_category in new_categories:
        row["Category"] = new_categories[row_category]

    return row
```

At the end of this, I rewrite the categorized transactions as CSVs again.

In the end the output CSVs looks the same as the input CSVs, except that the checking CSV has a new "Category" column and the credit card CSV has an updated "Category" column

# Build Chart and Table CSVs

Ok, the next steps are to combine these CSVs and build some MOAR CSVs. I can  render into a chart using [bbkane/tablegraph](https://github.com/bbkane/tablegraph/) (see next section for more info on `tablegraph`).

This is where Polars comes in! The first thing I do is read these CSVs in and combine them:

```python
    cc_trs_all = (
        pl.read_csv(cc_csv_path, sep="\t")
        .rename(
            {
                "Transaction Date": "tr_date",
                "Post Date": "post_date",
                "Description": "description",
                "Category": "category",
                "Trans. Amount": "tr_amount",
            }
        )
        .with_column(pl.col("tr_date").str.strptime(pl.Date, "%m/%d/%Y"))
        # * -1 : make purchases negative, paying off the card positive
        .with_column(pl.col("tr_amount").str.replace_all(r"[$,]", "").cast(pl.Float64) * -1)
        .with_column(pl.lit("credit_card").alias("source"))
        .sort("tr_date")
    )

    check_trs_all = (
        pl.read_csv(categorized_checking_tsv_path, sep="\t")
        .rename(
            {
                "Date": "tr_date",
                "Description": "description",
                "Comments": "comments",
                "Check Number": "check_number",
                "Amount": "tr_amount",
                "Balance": "balance",
                # no need to rename category
            }
        )
        .with_column(pl.col("tr_date").str.strptime(pl.Date, "%m/%d/%Y"))
        .with_column(pl.col("tr_amount").str.replace_all(r"[$,]", "").cast(pl.Float64))
        .with_column(pl.lit("checking").alias("source"))
    )

    trs_all = pl.concat(
        [
            cc_trs_all.select(("tr_date", "source", "category", "description", "tr_amount")),
            check_trs_all.select(("tr_date", "source", "category", "description", "tr_amount")),
        ]
    ).sort("tr_date")
```

I find most of thise code very easy to reason about! It does some renames and turns money values into floats (which are good enough for my banking) and then jams them together.

Now write more Polars code to build the CSVs (actually TSVs at this point) I need for my report. Most of these are a couple of lines long.

These use a small helper function to write the TSV

```python
def write_tsv(df: pl.DataFrame, workdir_path: str | pathlib.Path, file_name: str) -> None:
    df.write_csv(
        pathlib.Path(workdir_path, file_name),
        sep="\t",
    )
```

## Month So Far Costs By Category Table

```python
    month_so_far_costs_by_category = (
        trs_all.filter(pl.col("tr_date") >= first_of_month)
        .select(["category", "tr_amount"])
        .groupby("category")
        .agg(
            [
                pl.col("tr_amount").sum().alias("total").round(2),
                pl.col("tr_amount").count().alias("count"),
            ]
        )
        .sort("category")
    )

    write_tsv(month_so_far_costs_by_category, workdir_path, "month_so_far_costs_by_category.tsv")
```

## Profit Per Month Column Chart

```python
    monthly_profit_all = (
        trs_all.filter(pl.col("category") != "Int Account Transfer")
        .select(["tr_date", "tr_amount"])
        # TODO: optimize this? the strings are already lexigraphically sortable
        .with_column(pl.col("tr_date").dt.strftime("%Y-%m-15").str.strptime(pl.Date, "%Y-%m-%d"))
        .groupby("tr_date")
        .agg(pl.col("tr_amount").sum().alias("total").round(2))
        .with_column(pl.lit("profit").alias("type"))
        .select(["tr_date", "type", "total"])
        .sort("tr_date")
    )
  
    write_tsv(monthly_profit_all, workdir_path, "monthly_profit_all.tsv")
```

I've got a few more pretty similar expressions to make similar charts and tables.

# Render CSVs into Final Report

Finally, the last step is to take all these CSVs and write the final HTML using [tablegraph](https://github.com/bbkane/tablegraph/).

`tablegraph` is a small CLI tool I wrote to build [vega-lite](https://vega.github.io/vega-lite/) HTML charts out of specially-structured CSVs and [DataTables](https://datatables.net/) HTML tables out of other CSVs. It's not well documented, and to be honest, I've had some trouble with the chart generation, so at some point I might rewrite it. But for now, it works okay.

The first step is to define some helper functions:

```python
    with open(args.report_path, "w", encoding="utf-8") as fp:

        def report_print(args: ty.Sequence[ty.Any]) -> None:
            print(args, file=fp)
            fp.flush()

        def report_run(*args: str) -> None:
            subprocess.run(args, check=True, stdout=fp)

        def report_table(tsv: str) -> None:
            report_run(
                args.tablegraph_path,
                "--fieldnames",
                "firstline",
                "--fieldsep",
                "\t",
                "--format",
                "div",
                "--input",
                tsv,
                "--page-length",
                page_length,
                "table",
            )
```

Next, I simply call those functions to write to the file! Some examples:

```python
        # -- All time

        report_print("<center><h1>All Time</h1></center>")

        report_print("<center><h2>Transactions &gt; $500 </h2></center>")
        report_table(
            f"{args.workdir_path}/expensive_trs_all.tsv",
        )

        report_print("<center><h2>Profit per Month</h2></center>")

        # fmt: off
        report_run(
            args.tablegraph_path,
            "graph",
            "--div-width", "100%",
            "--fieldnames", "firstline",
            "--fieldsep", "\t",
            "--format", "div",
            "--graph-title", "Profit per Month",
            "--input", f"{args.workdir_path}/monthly_profit_all.tsv",
            "--mark-size", "5",
            "--type", "stacked-bar",
            "--x-scale-type", "utc",
            "--x-time-unit", "utcyearmonth",
            "--x-type", "temporal",
            "--y-type", "quantitative",
        )
        # fmt: on
```

At this point, i can open the report and read it, sometimes fixing categorization and re-running the report generation.

# Conclusions / Learnings

- The "data transformation as scripts reading and producing CSVs" approach works really well for this type of problem
  - Debugging discrete steps with input files available is easier than debugging an alternative "completely process in-memory and output the final HTML" process
  - I can easily intertwine different languages and methods for different stages of the pipeline. For example, I've rewritten the "Build Chart and Table CSVs" from [Nushell](https://www.nushell.sh/) to Polars, and the "Render CSVs into Final Report" step from python (with Plotly) to Go.
- This doesn't cover expenses that come out of my paycheck *before* the paycheck is deposited, like taxes and insurance through my employer, or investment gains/losses.
- Python is really good at data-sciency work like this. Polars is really great, I can't imagine doing this in Go. At the same time, I wish I had Go's excellent tooling, especially the packaging stuff so I could use Homebrew to package this tool for myself
- I'm not super delighted with either the general layout of the report (a lot of scrolling) or the charts Vega-Lite produces. Some more experimenting to be done there, as long as the result doesn't compromise the simplicity of the app.
- I've had a lot more fun building this than actually using it. Budgeting is hard :stuck_out_tongue: and I don't like downloading spreadsheets. I tell myself that, if I make this neato tool, I'll be able to manage my money so much better, but the truth is it takes daily spending discipline  and monthly tracking discipline to pull off budgeting.
