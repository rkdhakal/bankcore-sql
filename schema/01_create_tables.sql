-- =============================================================
-- BankCore SQL Project
-- File: 01_create_tables.sql
-- Description: Creates all 7 tables for the Canadian banking schema
-- Database: MySQL
-- =============================================================

CREATE DATABASE IF NOT EXISTS bankcore;
USE bankcore;

-- -------------------------------------------------------------
-- 1. BRANCHES
-- -------------------------------------------------------------
CREATE TABLE branches (
    branch_id       INT             AUTO_INCREMENT PRIMARY KEY,
    branch_name     VARCHAR(100)    NOT NULL,
    city            VARCHAR(100)    NOT NULL,
    province        CHAR(2)         NOT NULL,   -- e.g. ON, BC, AB, QC
    postal_code     VARCHAR(7)      NOT NULL,   -- e.g. M5V 3A8
    phone           VARCHAR(15),
    opened_date     DATE            NOT NULL
);

-- -------------------------------------------------------------
-- 2. CUSTOMERS
-- -------------------------------------------------------------
CREATE TABLE customers (
    customer_id     INT             AUTO_INCREMENT PRIMARY KEY,
    first_name      VARCHAR(50)     NOT NULL,
    last_name       VARCHAR(50)     NOT NULL,
    email           VARCHAR(100)    NOT NULL UNIQUE,
    phone           VARCHAR(15),
    date_of_birth   DATE            NOT NULL,
    sin_last4       CHAR(4),                    -- Last 4 digits of SIN (masked)
    city            VARCHAR(100)    NOT NULL,
    province        CHAR(2)         NOT NULL,
    postal_code     VARCHAR(7),
    credit_score    INT             CHECK (credit_score BETWEEN 300 AND 900),
    is_active       TINYINT         NOT NULL DEFAULT 1,  -- 1 = Active, 0 = Inactive (soft delete)
    created_at      DATE            NOT NULL,
    branch_id       INT             NOT NULL,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

-- -------------------------------------------------------------
-- 3. ACCOUNTS
-- -------------------------------------------------------------
CREATE TABLE accounts (
    account_id      INT             AUTO_INCREMENT PRIMARY KEY,
    customer_id     INT             NOT NULL,
    branch_id       INT             NOT NULL,
    account_type    VARCHAR(20)     NOT NULL,   -- Chequing, Savings, TFSA, RRSP, FHSA, GIC
    balance         DECIMAL(15,2)   NOT NULL DEFAULT 0.00,
    interest_rate   DECIMAL(5,2)    DEFAULT 0.00,
    opened_date     DATE            NOT NULL,
    status          VARCHAR(10)     NOT NULL DEFAULT 'Active',  -- Active, Closed, Frozen
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (branch_id)   REFERENCES branches(branch_id),
    CONSTRAINT chk_account_type CHECK (account_type IN ('Chequing','Savings','TFSA','RRSP','FHSA','GIC')),
    CONSTRAINT chk_account_status CHECK (status IN ('Active','Closed','Frozen'))
);

-- -------------------------------------------------------------
-- 4. TRANSACTIONS
-- -------------------------------------------------------------
CREATE TABLE transactions (
    transaction_id      INT             AUTO_INCREMENT PRIMARY KEY,
    account_id          INT             NOT NULL,
    branch_id           INT,
    transaction_type    VARCHAR(25)     NOT NULL,  -- Deposit, Withdrawal, Transfer, Bill Payment, Interac e-Transfer
    amount              DECIMAL(15,2)   NOT NULL CHECK (amount > 0),
    balance_after       DECIMAL(15,2)   NOT NULL,
    transaction_date    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description         VARCHAR(255),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (branch_id)  REFERENCES branches(branch_id),
    CONSTRAINT chk_txn_type CHECK (transaction_type IN ('Deposit','Withdrawal','Transfer','Bill Payment','Interac e-Transfer'))
);

-- -------------------------------------------------------------
-- 5. LOANS
-- -------------------------------------------------------------
CREATE TABLE loans (
    loan_id             INT             AUTO_INCREMENT PRIMARY KEY,
    customer_id         INT             NOT NULL,
    branch_id           INT             NOT NULL,
    loan_type           VARCHAR(20)     NOT NULL,  -- Mortgage, HELOC, Personal, Auto, Student
    principal_amount    DECIMAL(15,2)   NOT NULL CHECK (principal_amount > 0),
    interest_rate       DECIMAL(5,2)    NOT NULL,
    term_months         INT             NOT NULL,  -- e.g. 300 = 25 year mortgage
    monthly_payment     DECIMAL(15,2)   NOT NULL,
    start_date          DATE            NOT NULL,
    end_date            DATE            NOT NULL,
    status              VARCHAR(15)     NOT NULL DEFAULT 'Active',  -- Active, Paid Off, Defaulted, In Arrears
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (branch_id)   REFERENCES branches(branch_id),
    CONSTRAINT chk_loan_type CHECK (loan_type IN ('Mortgage','HELOC','Personal','Auto','Student')),
    CONSTRAINT chk_loan_status CHECK (status IN ('Active','Paid Off','Defaulted','In Arrears'))
);

-- -------------------------------------------------------------
-- 6. CARDS
-- -------------------------------------------------------------
CREATE TABLE cards (
    card_id             INT             AUTO_INCREMENT PRIMARY KEY,
    account_id          INT             NOT NULL,
    customer_id         INT             NOT NULL,
    card_type           VARCHAR(10)     NOT NULL,  -- Debit, Credit
    card_number_masked  VARCHAR(20)     NOT NULL,  -- e.g. ************1234
    credit_limit        DECIMAL(15,2)   DEFAULT NULL,  -- NULL for debit cards
    expiry_date         DATE            NOT NULL,
    status              VARCHAR(10)     NOT NULL DEFAULT 'Active',  -- Active, Blocked, Expired, Cancelled
    FOREIGN KEY (account_id)  REFERENCES accounts(account_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT chk_card_type CHECK (card_type IN ('Debit','Credit')),
    CONSTRAINT chk_card_status CHECK (status IN ('Active','Blocked','Expired','Cancelled'))
);

-- -------------------------------------------------------------
-- 7. LOAN PAYMENTS
-- -------------------------------------------------------------
CREATE TABLE loan_payments (
    payment_id          INT             AUTO_INCREMENT PRIMARY KEY,
    loan_id             INT             NOT NULL,
    payment_date        DATE            NOT NULL,
    amount_paid         DECIMAL(15,2)   NOT NULL CHECK (amount_paid > 0),
    principal_portion   DECIMAL(15,2)   NOT NULL,
    interest_portion    DECIMAL(15,2)   NOT NULL,
    remaining_balance   DECIMAL(15,2)   NOT NULL,
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id)
);

-- =============================================================
-- INDEXES ON FOREIGN KEY COLUMNS
-- (MySQL does not auto-index FK columns — needed for JOIN performance)
-- =============================================================
CREATE INDEX idx_customers_branch       ON customers(branch_id);
CREATE INDEX idx_accounts_customer      ON accounts(customer_id);
CREATE INDEX idx_accounts_branch        ON accounts(branch_id);
CREATE INDEX idx_transactions_account   ON transactions(account_id);
CREATE INDEX idx_transactions_branch    ON transactions(branch_id);
CREATE INDEX idx_transactions_date      ON transactions(transaction_date);
CREATE INDEX idx_loans_customer         ON loans(customer_id);
CREATE INDEX idx_loans_branch           ON loans(branch_id);
CREATE INDEX idx_cards_account          ON cards(account_id);
CREATE INDEX idx_cards_customer         ON cards(customer_id);
CREATE INDEX idx_loan_payments_loan     ON loan_payments(loan_id);
CREATE INDEX idx_loan_payments_date     ON loan_payments(payment_date);
