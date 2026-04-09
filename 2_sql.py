import re
import json
import sqlite3


def fix_quotes(text):
    return re.sub(r'(?<=\w)"(?=\w)', r'\\"', text)


def load_data(file_path):
    data = []
    invalid = []

    print("Loading data")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    items = re.split(r'},\s*{', content)

    for item in items:
        item = item.strip()

        if not item.startswith('{'):
            item = '{' + item
        if not item.endswith('}'):
            item = item + '}'

        item = re.sub(r':(\w+)=>', r'"\1":', item)

        item = fix_quotes(item)

        item = item.replace("'", '"')

        try:
            obj = json.loads(item)
            data.append(obj)
        except:
            invalid.append(item)

    print(f"Loaded valid records: {len(data)}")
    print(f"Skipped invalid records: {len(invalid)}")

    with open('bad_records.txt', 'w', encoding='utf-8') as f:
        for row in invalid:
            f.write(row + '\n')

    return data


def create_and_load_db(data):
    print("Creating DB and inserting data...")

    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS books")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id TEXT,
        title TEXT,
        author TEXT,
        genre TEXT,
        publisher TEXT,
        year INTEGER,
        price TEXT
    )
    """)

    cur.execute("DELETE FROM books")

    rows = [
        (
            str(book.get('id')),
            book.get('title'),
            book.get('author'),
            book.get('genre'),
            book.get('publisher'),
            book.get('year'),
            book.get('price')
        )
        for book in data
    ]

    cur.executemany("""
        INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    print(f"Inserted {len(rows)} records")

    cur.execute("DROP TABLE IF EXISTS summary")

    cur.execute("""
    CREATE TABLE summary AS
    SELECT
        year AS publication_year,
        COUNT(*) AS book_count,
        ROUND(
            AVG(
                CASE
                    WHEN price LIKE '€%' THEN
                        CAST(REPLACE(price, '€', '') AS REAL) * 1.2
                    WHEN price LIKE '$%' THEN
                        CAST(REPLACE(price, '$', '') AS REAL)
                END
            ), 2
        ) AS average_price_usd
    FROM books
    GROUP BY year
    """)

    conn.commit()
    print("Summary table created")

    cur.execute("SELECT COUNT(*) FROM books")
    print("Books count:", cur.fetchone()[0])

    cur.execute("SELECT COUNT(*) FROM summary")
    print("Summary count:", cur.fetchone()[0])

    print("\nSample summary:")
    for row in cur.execute("SELECT * FROM summary LIMIT 5"):
        print(row)

    conn.close()

if __name__ == "__main__":
    print("Script started")

    file_path = "task1_d.json"

    data = load_data(file_path)
    create_and_load_db(data)

    print("done!")