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
    drop_tables = [
        "DROP TABLE IF EXISTS `transaction_inventory_item`;",
        "DROP TABLE IF EXISTS `trip_employee`;",
        "DROP TABLE IF EXISTS `booking`;",
        "DROP TABLE IF EXISTS `transaction`;",
        "DROP TABLE IF EXISTS `trip`;",
        "DROP TABLE IF EXISTS `inventory_item`;",
        "DROP TABLE IF EXISTS `employee`;",
        "DROP TABLE IF EXISTS `experience`;",
        "DROP TABLE IF EXISTS `customer`;",
        "DROP TABLE IF EXISTS `region`;",
    ]

    create_tables = [
        """
        CREATE TABLE IF NOT EXISTS `region` (
            `region_id` INT AUTO_INCREMENT PRIMARY KEY,
            `region_name` VARCHAR(100) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS `customer` (
            `customer_id` INT AUTO_INCREMENT PRIMARY KEY,
            `first_name` VARCHAR(100) NOT NULL,
            `last_name` VARCHAR(100) NOT NULL,
            `email` VARCHAR(255),
            `phone` VARCHAR(25)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS `employee` (
            `employee_id` INT AUTO_INCREMENT PRIMARY KEY,
            `first_name` VARCHAR(100) NOT NULL,
            `last_name` VARCHAR(100) NOT NULL,
            `role` ENUM('Guide','Marketing','Inventory','Ecommerce','Admin') NOT NULL,
            `email` VARCHAR(255),
            `phone` VARCHAR(25)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS `experience` (
            `experience_id` INT AUTO_INCREMENT PRIMARY KEY,
            `region_id` INT NOT NULL,
            `experience_name` VARCHAR(150) NOT NULL,
            `description` TEXT,
            CONSTRAINT `fk_experience_region`
                FOREIGN KEY (`region_id`) REFERENCES `region`(`region_id`)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS `trip` (
            `trip_id` INT AUTO_INCREMENT PRIMARY KEY,
            `experience_id` INT NOT NULL,
            `date` DATE NOT NULL,
            `capacity` INT NOT NULL,
            `price` DECIMAL(10,2) NOT NULL,
            CONSTRAINT `fk_trip_experience`
                FOREIGN KEY (`experience_id`) REFERENCES `experience`(`experience_id`)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS `booking` (
            `booking_id` INT AUTO_INCREMENT PRIMARY KEY,
            `customer_id` INT NOT NULL,
            `trip_id` INT NOT NULL,
            `status` ENUM('Confirmed','Cancelled','Rescheduled','Complete') NOT NULL,
            CONSTRAINT `fk_booking_customer`
                FOREIGN KEY (`customer_id`) REFERENCES `customer`(`customer_id`),
            CONSTRAINT `fk_booking_trip`
                FOREIGN KEY (`trip_id`) REFERENCES `trip`(`trip_id`)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS `trip_employee` (
            `trip_employee_id` INT AUTO_INCREMENT PRIMARY KEY,
            `trip_id` INT NOT NULL,
            `employee_id` INT NOT NULL,
            CONSTRAINT `fk_trip_employee_trip`
                FOREIGN KEY (`trip_id`) REFERENCES `trip`(`trip_id`),
            CONSTRAINT `fk_trip_employee_employee`
                FOREIGN KEY (`employee_id`) REFERENCES `employee`(`employee_id`),
            UNIQUE KEY `uq_trip_employee` (`trip_id`, `employee_id`)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS `inventory_item` (
            `item_id` INT AUTO_INCREMENT PRIMARY KEY,
            `item_name` VARCHAR(150) NOT NULL,
            `description` TEXT,
            `status` ENUM('Available','Rented','Sold','Pulled') NOT NULL,
            `expected_return_date` DATE,
            `sale_price` DECIMAL(10,2),
            `rental_price` DECIMAL(10,2),
            `acquisition_date` DATE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS `transaction` (
            `transaction_id` INT AUTO_INCREMENT PRIMARY KEY,
            `customer_id` INT NOT NULL,
            `date` DATE NOT NULL,
            `total` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
            CONSTRAINT `fk_transaction_customer`
                FOREIGN KEY (`customer_id`) REFERENCES `customer`(`customer_id`)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS `transaction_inventory_item` (
            `line_item_id` INT AUTO_INCREMENT PRIMARY KEY,
            `transaction_id` INT NOT NULL,
            `item_id` INT NOT NULL,
            `transaction_type` ENUM('Rental','Purchase') NOT NULL,
            `rental_start_date` DATE,
            `rental_end_date` DATE,
            `return_date` DATE,
            `line_price` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
            CONSTRAINT `fk_line_transaction`
                FOREIGN KEY (`transaction_id`) REFERENCES `transaction`(`transaction_id`),
            CONSTRAINT `fk_line_item`
                FOREIGN KEY (`item_id`) REFERENCES `inventory_item`(`item_id`)
        );
        """,
    ]

    db = None
    cursor = None

    try:
        print("Connecting to database...")
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        print("Dropping tables...")
        for sql in drop_tables:
            cursor.execute(sql)

        print("Creating tables...")
        for sql in create_tables:
            cursor.execute(sql)

        db.commit()
        print("Tables created.")

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