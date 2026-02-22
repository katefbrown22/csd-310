import mysql.connector
from dotenv import dotenv_values

secrets = dotenv_values(".env")

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": False
}


def main():
    db = None
    cursor = None

    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        regions = [
            ("North America",),
            ("South America",),
            ("Europe",),
            ("Africa",),
            ("Asia",),
            ("Oceania",),
        ]
        cursor.executemany("INSERT INTO region (region_name) VALUES (%s);", regions)

        employees = [
            ("Blythe", "Timmerson", "Admin",     "blythe@outland.com",      "555-0101"),
            ("Jim",    "Ford",      "Admin",     "jim@outland.com",         "555-0102"),
            ("John",   "MacNell",   "Guide",     "mac@outland.com",         "555-0103"),
            ("D.B.",   "Marland",   "Guide",     "duke@outland.com",        "555-0104"),
            ("Anita",  "Gallegos",  "Marketing", "anita@outland.com",       "555-0105"),
            ("Dimitrios", "Stravopolous", "Inventory", "dimitrios@outland.com", "555-0106"),
        ]
        cursor.executemany(
            """
            INSERT INTO employee (first_name, last_name, role, email, phone)
            VALUES (%s, %s, %s, %s, %s);
            """,
            employees
        )

        customers = [
            ("Alex",   "Rivera",   "alex.rivera@email.com",    "555-1001"),
            ("Morgan", "Lee",      "morgan.lee@email.com",     "555-1002"),
            ("Jordan", "Patel",    "jordan.patel@email.com",   "555-1003"),
            ("Casey",  "Nguyen",   "casey.nguyen@email.com",   "555-1004"),
            ("Taylor", "Johnson",  "taylor.johnson@email.com", "555-1005"),
            ("Riley",  "Martinez", "riley.martinez@email.com", "555-1006"),
        ]
        cursor.executemany(
            """
            INSERT INTO customer (first_name, last_name, email, phone)
            VALUES (%s, %s, %s, %s);
            """,
            customers
        )

        experiences = [
            (1, "Banff National Park Backpacking (Canada)", "Multi-day backpacking through alpine terrain and glacial lakes."),
            (2, "Torres del Paine Circuit (Chile)", "Patagonia trekking with strong winds and rugged trails."),
            (3, "Plitvice Lakes National Park Hike (Croatia)", "Waterfalls, boardwalk trails, and scenic day hikes."),
            (4, "Serengeti National Park Trek (Tanzania)", "Guided trekking and wildlife safety orientation."),
            (5, "Sagarmatha National Park Trek (Nepal)", "High-altitude trekking with acclimatization planning."),
            (6, "Fiordland National Park Track (New Zealand)", "Rainforest and fjord landscapes with wet-weather conditions."),
        ]
        cursor.executemany(
            """
            INSERT INTO experience (region_id, experience_name, description)
            VALUES (%s, %s, %s);
            """,
            experiences
        )

        trips = [
            (1, "2026-03-20", 12, 1099.99),
            (2, "2026-04-10", 10, 1499.99),
            (3, "2026-04-25", 16,  799.99),
            (4, "2026-05-15",  8, 1599.99),
            (5, "2026-06-05", 10, 1799.99),
            (6, "2026-06-20", 14, 1199.99),
        ]
        cursor.executemany(
            """
            INSERT INTO trip (experience_id, date, capacity, price)
            VALUES (%s, %s, %s, %s);
            """,
            trips
        )

        bookings = [
            (1, 1, "Confirmed"),
            (2, 2, "Confirmed"),
            (3, 3, "Rescheduled"),
            (4, 4, "Cancelled"),
            (5, 5, "Confirmed"),
            (6, 6, "Complete"),
        ]
        cursor.executemany(
            """
            INSERT INTO booking (customer_id, trip_id, status)
            VALUES (%s, %s, %s);
            """,
            bookings
        )

        trip_employees = [
            (1, 3),
            (2, 4),
            (3, 3),
            (4, 4),
            (5, 3),
            (6, 4),
        ]
        cursor.executemany(
            """
            INSERT INTO trip_employee (trip_id, employee_id)
            VALUES (%s, %s);
            """,
            trip_employees
        )

        inventory_items = [
            ("65L Backpack", "Internal-frame backpack suitable for multi-day treks.", "Available", None, 189.99, 24.99, "2025-05-10"),
            ("2 Person Backpacking Tent", "Lightweight tent with rainfly.", "Available", None, 329.99, 39.99, "2019-07-18"),
            ("Trekking Poles", "Adjustable aluminum trekking poles.", "Available", None, 59.99, 9.99, "2024-03-02"),
            ("Sleeping Bag", "Three-season sleeping bag rated to ~20°F.", "Available", None, 149.99, 19.99, "2018-10-12"),
            ("Headlamp", "LED headlamp with spare batteries included.", "Available", None, 29.99, 4.99, "2023-06-01"),
            ("Portable Water Filter", "Inline filter for backcountry water sources.", "Available", None, 39.99, 6.99, "2021-08-25"),
        ]
        cursor.executemany(
            """
            INSERT INTO inventory_item
            (item_name, description, status, expected_return_date, sale_price, rental_price, acquisition_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            inventory_items
        )

        transactions = [
            (1, "2026-02-23", 34.98),
            (2, "2026-02-24", 329.99),
            (3, "2026-02-25", 19.99),
            (4, "2026-02-26", 59.99),
            (5, "2026-02-27", 11.98),
            (6, "2026-02-28", 39.99),
        ]
        cursor.executemany(
            """
            INSERT INTO `transaction` (customer_id, date, total)
            VALUES (%s, %s, %s);
            """,
            transactions
        )

        line_items = [
            (1, 3, "Rental",   "2026-03-18", "2026-03-24", None,  9.99),
            (1, 5, "Rental",   "2026-03-18", "2026-03-24", None,  4.99),
            (2, 2, "Purchase", None, None, None, 329.99),
            (3, 4, "Rental",   "2026-04-20", "2026-04-28", None, 19.99),
            (4, 3, "Purchase", None, None, None, 59.99),
            (6, 6, "Purchase", None, None, None, 39.99),
        ]
        cursor.executemany(
            """
            INSERT INTO transaction_inventory_item
            (transaction_id, item_id, transaction_type, rental_start_date, rental_end_date, return_date, line_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            line_items
        )

        cursor.execute("""
            UPDATE inventory_item
            SET status='Rented', expected_return_date='2026-03-24'
            WHERE item_id=5;
        """)
        cursor.execute("""
            UPDATE inventory_item
            SET status='Rented', expected_return_date='2026-04-28'
            WHERE item_id=4;
        """)
        cursor.execute("""
            UPDATE inventory_item
            SET status='Sold'
            WHERE item_id IN (2, 3, 6);
        """)

        db.commit()
        print("Done adding data")

        print("\n--- REGION ---")
        cursor.execute("SELECT * FROM region;")
        for row in cursor.fetchall():
            print(row)

        print("\n--- CUSTOMER ---")
        cursor.execute("SELECT * FROM customer;")
        for row in cursor.fetchall():
            print(row)

        print("\n--- EMPLOYEE ---")
        cursor.execute("SELECT * FROM employee;")
        for row in cursor.fetchall():
            print(row)

        print("\n--- EXPERIENCE ---")
        cursor.execute("SELECT * FROM experience;")
        for row in cursor.fetchall():
            print(row)

        print("\n--- TRIP ---")
        cursor.execute("SELECT * FROM trip;")
        for row in cursor.fetchall():
            print(row)

        print("\n--- BOOKING ---")
        cursor.execute("SELECT * FROM booking;")
        for row in cursor.fetchall():
            print(row)

        print("\n--- TRIP_EMPLOYEE ---")
        cursor.execute("SELECT * FROM trip_employee;")
        for row in cursor.fetchall():
            print(row)

        print("\n--- INVENTORY_ITEM ---")
        cursor.execute("SELECT * FROM inventory_item;")
        for row in cursor.fetchall():
            print(row)

        print("\n--- TRANSACTION ---")
        cursor.execute("SELECT * FROM `transaction`;")
        for row in cursor.fetchall():
            print(row)

        print("\n--- TRANSACTION_INVENTORY_ITEM ---")
        cursor.execute("SELECT * FROM transaction_inventory_item;")
        for row in cursor.fetchall():
            print(row)

    except Exception as e:
        print("Error:")
        print(e)

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


if __name__ == "__main__":
    main()