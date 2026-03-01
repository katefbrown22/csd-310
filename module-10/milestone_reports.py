

import mysql.connector
from dotenv import dotenv_values

secrets = dotenv_values(".env")

config = {
    "user": secrets.get("USER"),
    "password": secrets.get("PASSWORD"),
    "host": secrets.get("HOST"),
    "database": secrets.get("DATABASE"),
    "raise_on_warnings": False,
}


def print_rows(title: str, columns: list[str], rows: list[tuple]) -> None:
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)

    if not rows:
        print("(No rows returned)")
        return

    widths = [len(c) for c in columns]
    for r in rows[:50]:
        for i, v in enumerate(r):
            widths[i] = max(widths[i], len("" if v is None else str(v)))

    def fmt(vals):
        return " | ".join((("" if v is None else str(v)).ljust(widths[i]) for i, v in enumerate(vals)))

    print(fmt(columns))
    print("-" * (sum(widths) + 3 * (len(widths) - 1)))

    for r in rows[:50]:
        print(fmt(r))

    if len(rows) > 50:


REPORTS = [
    {
        # Case study question: Do enough customers buy equipment to keep equipment sales?
        "name": "Report 1-Equipment sales vs rentals",
        "columns": ["transaction_type", "line_items", "revenue", "avg_line_price", "pct_of_revenue"],
        "sql": """
            WITH totals AS (
                SELECT ROUND(SUM(line_price), 2) AS total_revenue
                FROM transaction_inventory_item
            ),
            by_type AS (
                SELECT
                    transaction_type,
                    COUNT(*) AS line_items,
                    ROUND(SUM(line_price), 2) AS revenue,
                    ROUND(AVG(line_price), 2) AS avg_line_price
                FROM transaction_inventory_item
                GROUP BY transaction_type
            )
            SELECT
                b.transaction_type,
                b.line_items,
                b.revenue,
                b.avg_line_price,
                ROUND((b.revenue / NULLIF(t.total_revenue, 0)) * 100, 1) AS pct_of_revenue
            FROM by_type b
            CROSS JOIN totals t
            ORDER BY b.revenue DESC;
        """
    },
    {
        # Case study question: Is there any one of those locations that has a downward trend in bookings?
        "name": "Report 2-Booking trend by region",
        "columns": ["region", "month", "confirmed_bookings", "change_vs_prior_month"],
        "sql": """
            WITH monthly AS (
                SELECT
                    r.region_name AS region,
                    DATE_FORMAT(t.date, '%Y-%m') AS month,
                    COUNT(*) AS confirmed_bookings
                FROM booking b
                JOIN trip t ON b.trip_id = t.trip_id
                JOIN experience e ON t.experience_id = e.experience_id
                JOIN region r ON e.region_id = r.region_id
                WHERE b.status = 'Confirmed'
                  AND r.region_name IN ('Africa', 'Asia', 'Southern Europe')
                GROUP BY r.region_name, DATE_FORMAT(t.date, '%Y-%m')
            )
            SELECT
                region,
                month,
                confirmed_bookings,
                confirmed_bookings - LAG(confirmed_bookings) OVER (PARTITION BY region ORDER BY month) AS change_vs_prior_month
            FROM monthly
            ORDER BY region, month;
        """
    },
    {
        # Case study question: Are there inventory items that are over five years old?
        "name": "Report 3-Inventory older than 5 years",
        "columns": ["item_id", "item_name", "status", "acquisition_date", "age_years"],
        "sql": """
            SELECT
                item_id,
                item_name,
                status,
                acquisition_date,
                ROUND(DATEDIFF(CURDATE(), acquisition_date) / 365.25, 2) AS age_years
            FROM inventory_item
            WHERE acquisition_date IS NOT NULL
              AND acquisition_date <= (CURDATE() - INTERVAL 5 YEAR)
            ORDER BY acquisition_date ASC, item_name;
        """
    },
]


def main() -> None:
    db = None
    cursor = None

    try:
        print("Connecting")
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        for report in REPORTS:
            cursor.execute(report["sql"])
            rows = cursor.fetchall()
            print_rows(report["name"], report["columns"], rows)

    except Exception as e:
        print("\nERROR running reports:")
        print(e)
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


if __name__ == "__main__":
    main()
