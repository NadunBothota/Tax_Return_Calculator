CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    password TEXT NOT NULL
);

CREATE TABLE user_tax_records (
    id SERIAL PRIMARY KEY,
    person_id VARCHAR(6) NOT NULL,
    tfn VARCHAR(8),
    income REAL NOT NULL,
    tax_withheld REAL NOT NULL,
    has_phic BOOLEAN NOT NULL,
    tax REAL NOT NULL,
    medicare_levy REAL NOT NULL,
    medicare_levy_surcharge REAL NOT NULL,
    refund_or_payable REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tax_data (
    tfn TEXT,
    income REAL,
    withheld REAL
);


INSERT INTO users (username, password) VALUES
('nadun123', 'password123'),
('amal456', 'securepass'),
('sara789', 'mypassword'),
('kumar001', 'letmein'),
('nisha007', 'pa$$w0rd');


INSERT INTO user_tax_records
(person_id, tfn, income, tax_withheld, has_phic, tax, medicare_levy, medicare_levy_surcharge, refund_or_payable)
VALUES
('000001', '12345678', 75000, 15000, true, 12000, 1500, 0, 1500),
('000002', '87654321', 50000, 9000, false, 8000, 1000, 500, 500),
('000003', NULL, 62000, 11000, true, 10000, 1240, 0, 760),
('000004', '56781234', 45000, 8500, false, 7000, 900, 450, 150),
('000005', '43218765', 90000, 20000, true, 15000, 1800, 0, 1200);


INSERT INTO tax_data (tfn, income, withheld) VALUES
('12345678', 3000, 600),
('12345678', 3200, 640),
('87654321', 2500, 450),
('87654321', 2600, 470),
('56781234', 2200, 400),
('43218765', 3500, 700),
('43218765', 3600, 720);
