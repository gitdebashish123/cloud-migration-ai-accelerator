CREATE DATABASE sales_db
LOCATION '/user/hive/warehouse/sales_db.db';

USE sales_db;
CREATE TABLE employee_parquet (
  emp_id INT,
  emp_name STRING,
  department STRING,
  sales DOUBLE
)
STORED AS PARQUET
LOCATION '/user/hive/warehouse/sales_db.db/employee_parquet';


USE sales_db;
INSERT INTO TABLE employee_parquet VALUES
(101, 'Alice', 'HR', 55000.0),
(102, 'Bob', 'Engineering', 72000.0),
(103, 'Charlie', 'Finance', 64000.0),
(104, 'Diana', 'Engineering', 81000.0),
(105, 'Eve', 'Marketing', 59000.0);


USE sales_db;

CREATE TABLE sales_summary (
  sale_id INT,
  emp_id INT,
  product STRING,
  amount DOUBLE,
  sale_date DATE
)
STORED AS PARQUET
LOCATION '/user/hive/warehouse/sales_db.db/sales_summary';


USE sales_db;

INSERT INTO sales_summary (sale_id, emp_id, product, amount, sale_date) VALUES
  (1, 101, 'Laptop', 75000.00, DATE '2025-01-10'),
  (2, 102, 'Mobile', 25000.00, DATE '2025-01-12'),
  (3, 103, 'Headphones', 3000.00, DATE '2025-01-15'),
  (4, 101, 'Monitor', 12000.00, DATE '2025-01-18'),
  (5, 104, 'Keyboard', 2000.00, DATE '2025-01-20');


CREATE DATABASE transaction_db
LOCATION '/user/hive/warehouse/transaction_db.db';

USE transaction_db;


CREATE TABLE customers (
    customer_id INT,
    customer_name STRING,
    email STRING,
    city STRING
)
STORED AS PARQUET
LOCATION '/user/hive/warehouse/transaction_db.db/customers';

INSERT INTO TABLE customers VALUES
(1, 'Alice Johnson', 'alice@example.com', 'Bhubaneswar'),
(2, 'Ravi Kumar', 'ravi.kumar@example.com', 'Cuttack'),
(3, 'Sneha Patel', 'sneha.patel@example.com', 'Puri');


CREATE TABLE customers_txn (
    txn_id INT,
    customer_id INT,
    amount DECIMAL(10,2),
    txn_date STRING
)
STORED AS PARQUET
LOCATION '/user/hive/warehouse/transaction_db.db/customers_txn';


INSERT INTO TABLE customers_txn VALUES
(101, 1, 1200.50, '2025-10-27'),
(102, 2, 560.00, '2025-10-28'),
(103, 1, 230.75, '2025-10-29');