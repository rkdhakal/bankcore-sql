-- =============================================================
-- BankCore SQL Project - TD Canada Trust
-- Phase 3: JOINs & Subqueries
-- =============================================================

-- Q1. Risk team: all customers with an active mortgage, their credit
--     score, and the branch where the mortgage was issued.
--     Sort by credit score ascending (riskiest at top).

SELECT
    c.first_name,
    c.last_name,
    c.credit_score,
    b.branch_name
FROM customers c
INNER JOIN loans l ON c.customer_id = l.customer_id
INNER JOIN branches b ON l.branch_id = b.branch_id
WHERE l.loan_type = 'Mortgage'
  AND l.status = 'Active'
ORDER BY c.credit_score ASC;

-- -------------------------------------------------------------
-- Q2. Show all transactions above $5,000 with the customer's
--     full name, account type, and branch name.
-- (Pending)

-- -------------------------------------------------------------
-- Q3. List every loan payment made in 2024 with customer full
--     name, loan type, and amount paid.
-- (Pending)

-- -------------------------------------------------------------
-- Q4. Marketing: customers with TFSA or RRSP but no card issued.
--     Show name, email, account type.
-- (Pending)

-- -------------------------------------------------------------
-- Q5. Find all customers who have never taken any loan.
--     Show name, credit score, and date they joined TD.
-- (Pending)

-- -------------------------------------------------------------
-- Q6. List all accounts that have never had a single transaction.
--     Show account type, balance, and when it was opened.
-- (Pending)

-- -------------------------------------------------------------
-- Q7. Show all branches and total loans issued per branch.
--     Include branches with zero loans.
-- (Pending)

-- -------------------------------------------------------------
-- Q8. List all loan types and customers assigned to them.
--     Include loan types with no customers.
-- (Pending)

-- -------------------------------------------------------------
-- Q9. Data quality check: show all customers and all accounts
--     including customers with no accounts and accounts with
--     no linked customer.
-- (Pending)

-- -------------------------------------------------------------
-- Q10. Find pairs of customers at the same branch with the same
--      account type for cross-sell targeting.
-- (Pending)

-- -------------------------------------------------------------
-- Q11. Find customers who joined TD in the same year as another
--      customer at the same branch.
-- (Pending)

-- -------------------------------------------------------------
-- Q12. Generate a full matrix of all provinces x all loan types
--      for a product availability report template.
-- (Pending)

-- -------------------------------------------------------------
-- Q13. Find customers whose total balance across all accounts
--      is above the bank-wide average total balance per customer.
-- (Pending)

-- -------------------------------------------------------------
-- Q14. List the top 3 branches by total transaction volume.
-- (Pending)

-- -------------------------------------------------------------
-- Q15. Find customers who have more than 2 accounts at TD Bank.
-- (Pending)

-- -------------------------------------------------------------
-- Q16. Find all accounts whose balance is higher than the average
--      balance of ALL accounts in the bank.
-- (Pending)

-- -------------------------------------------------------------
-- Q17. For each customer, show their most recent transaction
--      date and amount.
-- (Pending)

-- -------------------------------------------------------------
-- Q18. Find accounts where balance is higher than the average
--      balance of accounts of the same type.
-- (Pending)

-- -------------------------------------------------------------
-- Q19. For each branch, find the customer with the highest
--      total balance — branch top depositor.
-- (Pending)

-- -------------------------------------------------------------
-- Q20. Find customers who have at least one transaction larger
--      than their account current balance — data quality flag.
-- (Pending)

-- -------------------------------------------------------------
-- Q21. Collections: customers with a defaulted loan whose total
--      account balance is less than $5,000 — highest risk.
-- (Pending)

-- -------------------------------------------------------------
-- Q22. Find branches where the average customer credit score
--      is below 650 — higher risk portfolio branches.
-- (Pending)

-- -------------------------------------------------------------
-- Q23. For each mortgage customer, show how many loan payments
--      made so far and remaining balance on latest payment.
-- (Pending)

-- -------------------------------------------------------------
-- Q24. Find customers who have made Interac e-Transfers to the
--      same recipient more than once — potential fraud pattern.
-- (Pending)

-- -------------------------------------------------------------
-- Q25. Executive 360 view: for each customer show full name,
--      total accounts, total balance, total transactions,
--      active loan (Yes/No), active card (Yes/No),
--      and credit score band (Poor/Fair/Good/Excellent).
-- (Pending)
