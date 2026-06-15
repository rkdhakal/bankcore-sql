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
#Q2. Marketing wants customers who have a TFSA or RRSP but have never been issued any card. Pull name, email, and account type.
USE bankcore;

SELECT 
    c.first_name,
    c.last_name,
    c.email,
    GROUP_CONCAT(a.account_type) as account_types
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
LEFT JOIN cards d ON c.customer_id = d.customer_id
WHERE d.customer_id IS NULL AND a.account_type IN ('TFSA', 'RRSP')
GROUP BY c.customer_id;

/*LEFT JOIN + NULL check — "never issued a card"
IN ('TFSA', 'RRSP') — correct multi-value filter
GROUP_CONCAT — collapses multiple account types into one row
GROUP BY c.customer_id — one row per customer
*/
/*Q3.The branch manager at each TD location wants to see how many active customers are registered at their branch and the total balance held across all those customers' accounts. Include branches even if they currently have zero customers.*/
USE bankcore;
SELECT 
b.branch_name,
COUNT(c.customer_id) AS active_customers,
SUM(a.balance) AS total_balance
 FROM branches b
LEFT JOIN customers c ON c.branch_id=b.branch_id AND  c.is_active = 1
LEFT JOIN accounts a ON a.customer_id = c.customer_id 
GROUP BY branch_name;

/*LEFT JOIN branches → customers — keeps branches with zero customers
AND c.is_active = 1 in the JOIN — filters inactive customers without killing empty branches
LEFT JOIN accounts ON a.customer_id = c.customer_id — balances tied to active customers only
GROUP BY b.branch_name — one row per branch */