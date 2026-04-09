# Data Engineering Task 1

## Description

In this task I worked with a dataset that is not a valid JSON file.
I cleaned and processed the data using Python, then loaded it into a relational database.

## Steps

1. **Data cleaning and ingestion using Python**
   I parsed the raw file, fixed its format, and skipped records that could not be processed.

2. **Loading data and SQL transformation**
   The cleaned data was loaded into an SQLite database.
   Then I used SQL (executed via Python) to create a summary table with the required metrics.

## Transformation logic

* Grouped data by publication year
* Counted number of books per year
* Calculated average price in USD
* Converted EUR to USD using rate €1 = $1.2
* Rounded results to 2 decimal places

## How to run

```bash
python 1_data_file.py
python 2_sql.py
```

## Notes

* Invalid records are saved in `bad_records.txt`
* The script can be run multiple times without errors
