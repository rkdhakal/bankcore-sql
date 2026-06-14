"""
BankCore SQL Project
File: generate_data.py
Description: Generates realistic TD Canada Trust banking data.
"""

import random
import calendar
from datetime import date, datetime, timedelta
from faker import Faker

fake = Faker('en_CA')
random.seed(42)
Faker.seed(42)

TODAY = date.today()

# ============================================================
# CONFIGURATION
# ============================================================
NUM_CUSTOMERS    = 500
NUM_TRANSACTIONS = 5000
NUM_LOANS        = 150
NUM_CARDS        = 300
OUTPUT_FILE      = "02_insert_data.sql"

# ============================================================
# TD CANADA TRUST BRANCHES
# ============================================================
BRANCHES = [
    (1,  "TD Canada Trust - King & Bay",           "Toronto",       "ON", "M5H 4A6", "416-982-2265"),
    (2,  "TD Canada Trust - Yonge & Bloor",         "Toronto",       "ON", "M4W 3R8", "416-982-2266"),
    (3,  "TD Canada Trust - Mississauga City Ctr",  "Mississauga",   "ON", "L5B 1M7", "905-306-5000"),
    (4,  "TD Canada Trust - Ottawa Rideau",          "Ottawa",        "ON", "K1N 9J7", "613-783-3200"),
    (5,  "TD Canada Trust - Vancouver Granville",    "Vancouver",     "BC", "V6C 1T2", "604-654-3600"),
    (6,  "TD Canada Trust - Victoria Douglas St",    "Victoria",      "BC", "V8W 2C3", "250-356-3500"),
    (7,  "TD Canada Trust - Calgary Downtown",       "Calgary",       "AB", "T2P 1J9", "403-292-8200"),
    (8,  "TD Canada Trust - Edmonton Jasper Ave",    "Edmonton",      "AB", "T5J 1X9", "780-423-3600"),
    (9,  "TD Canada Trust - Montreal Rene-Levesque", "Montreal",      "QC", "H3B 1S6", "514-289-0833"),
    (10, "TD Canada Trust - Quebec City St-Jean",    "Quebec City",   "QC", "G1R 1P8", "418-694-1000"),
    (11, "TD Canada Trust - Winnipeg Portage Ave",   "Winnipeg",      "MB", "R3C 0A5", "204-988-2300"),
    (12, "TD Canada Trust - Halifax Spring Garden",  "Halifax",       "NS", "B3J 3T2", "902-420-8400"),
    (13, "TD Canada Trust - Saskatoon 2nd Ave",      "Saskatoon",     "SK", "S7K 1K1", "306-975-5100"),
    (14, "TD Canada Trust - Fredericton Queen St",   "Fredericton",   "NB", "E3B 1B3", "506-452-5000"),
    (15, "TD Canada Trust - Charlottetown Main",     "Charlottetown", "PE", "C1A 4N6", "902-566-3400"),
]

BRANCH_OPENED = {
    1: date(2001, 3, 15),  2: date(1998, 6, 10),  3: date(2003, 9, 1),
    4: date(2000, 4, 22),  5: date(1999, 7, 14),  6: date(2002, 11, 5),
    7: date(2001, 8, 30),  8: date(2000, 1, 17),  9: date(1997, 5, 20),
   10: date(2004, 3, 8),  11: date(2002, 6, 25), 12: date(1999, 10, 3),
   13: date(2003, 2, 14), 14: date(2001, 7, 19), 15: date(2005, 4, 11),
}

PROVINCES = ["ON", "BC", "AB", "QC", "MB", "SK", "NS", "NB", "NL", "PE"]
PROVINCE_CITIES = {
    "ON": ["Toronto", "Ottawa", "Mississauga", "Hamilton", "London", "Brampton", "Markham"],
    "BC": ["Vancouver", "Victoria", "Surrey", "Burnaby", "Kelowna", "Abbotsford"],
    "AB": ["Calgary", "Edmonton", "Red Deer", "Lethbridge", "Medicine Hat"],
    "QC": ["Montreal", "Quebec City", "Laval", "Gatineau", "Sherbrooke"],
    "MB": ["Winnipeg", "Brandon", "Steinbach", "Thompson"],
    "SK": ["Saskatoon", "Regina", "Prince Albert", "Moose Jaw"],
    "NS": ["Halifax", "Sydney", "Truro", "New Glasgow"],
    "NB": ["Fredericton", "Moncton", "Saint John", "Bathurst"],
    "NL": ["St. John's", "Corner Brook", "Gander", "Grand Falls-Windsor"],
    "PE": ["Charlottetown", "Summerside", "Stratford"],
}

# ============================================================
# SCENARIO DEFINITIONS
# ============================================================
SCENARIO_MULTI_ACCOUNT  = range(100, 121)
SCENARIO_FHSA           = range(121, 141)
SCENARIO_HIGH_VALUE     = range(200, 211)
SCENARIO_DEFAULTED      = range(350, 361)
SCENARIO_IN_ARREARS     = range(361, 371)
SCENARIO_PAID_OFF       = range(371, 391)
SCENARIO_ETRANSFER      = range(300, 321)
SCENARIO_BLOCKED_CARD   = range(420, 441)
SCENARIO_FROZEN_ACCOUNT = range(460, 471)
SCENARIO_NO_LOAN        = range(480, 491)
SCENARIO_DORMANT        = range(491, 501)
SCENARIO_STUDENT        = range(1,   21)
SCENARIO_HIGH_CREDIT    = range(21,  71)

# ============================================================
# VALID TRANSACTION TYPES PER ACCOUNT (real banking rules)
# RRSP: 95% deposits/transfers, 5% withdrawals (taxable but allowed)
# ============================================================
VALID_TXN_TYPES = {
    "Chequing": ["Deposit", "Withdrawal", "Transfer", "Bill Payment", "Interac e-Transfer"],
    "Savings":  ["Deposit", "Withdrawal", "Transfer"],
    "TFSA":     ["Deposit", "Withdrawal", "Transfer"],
    "RRSP":     ["Deposit", "Transfer", "Withdrawal"],  # Withdrawal allowed but rare
    "FHSA":     ["Deposit", "Transfer"],
    "GIC":      [],
}

TXN_DESCRIPTIONS = {
    "Deposit": [
        "TD Direct Deposit - Payroll", "Cash deposit at TD branch",
        "CRA tax refund - direct deposit", "EI benefit payment",
        "CPP pension deposit", "OAS pension payment",
        "Interac e-Transfer received", "TD internal transfer received",
        "Government of Canada payment", "TD Direct Deposit - Bonus",
    ],
    "Withdrawal": [
        "TD Green Machine ATM withdrawal", "TD Branch cash withdrawal",
        "TD Access Card - cash back",
    ],
    "Transfer": [
        "Transfer to TD High Interest Savings", "Transfer to TD eSeries TFSA",
        "Transfer to TD Mutual Funds RRSP", "Transfer to TD Chequing",
        "TD EasyWeb online transfer", "TD internal transfer",
    ],
    "Bill Payment": [
        "Hydro One - account payment", "Rogers Communications bill",
        "Bell Canada bill payment", "Toronto Hydro payment",
        "Enbridge Gas payment", "TELUS Mobility bill",
        "Rogers Internet bill", "City of Toronto tax payment",
        "BC Hydro payment", "Fortis Alberta payment",
        "TD Insurance premium", "Property tax payment",
        "City of Calgary utility bill", "Enmax Energy payment",
        "Nova Scotia Power bill",
    ],
    "Interac e-Transfer": [],
    "RRSP Withdrawal": [
        "RRSP withdrawal - Home Buyers Plan",
        "RRSP withdrawal - Lifelong Learning Plan",
        "RRSP taxable withdrawal",
    ],
}

# ============================================================
# HELPERS
# ============================================================
def add_months(d, months):
    total = d.month - 1 + months
    year  = d.year + total // 12
    month = total % 12 + 1
    day   = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)

def rand_date_between(start, end):
    delta = (end - start).days
    if delta <= 0:
        return start
    return start + timedelta(days=random.randint(0, delta))

def rand_phone():
    return f"{random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}"

def rand_postal():
    L = "ABCEGHJKLMNPRSTVXY"
    return f"{random.choice(L)}{random.randint(1,9)}{random.choice(L)} {random.randint(1,9)}{random.choice(L)}{random.randint(1,9)}"

def calc_monthly_payment(principal, annual_rate_pct, term_months):
    r = annual_rate_pct / 100 / 12
    if r == 0:
        return round(principal / term_months, 2)
    return round(principal * r / (1 - (1 + r) ** (-term_months)), 2)

def months_between(d1, d2):
    return (d2.year - d1.year) * 12 + (d2.month - d1.month)

def esc(s):
    return str(s).replace("'", "''")

# FIX 3: Realistic transaction datetime with weekday bias + payroll pattern
def realistic_txn_datetime(start_date, end_date, txn_type):
    """
    - 80% of transactions fall on weekdays (Mon-Fri)
    - Payroll deposits cluster on 15th and last day of month
    - ATM withdrawals cluster on Friday afternoons and weekends
    """
    for _ in range(20):  # Try up to 20 times to get a valid date
        d = rand_date_between(start_date, end_date)

        if txn_type == "Deposit" and random.random() < 0.45:
            # Payroll: 15th or last day of month
            if random.random() < 0.5:
                day = 15
            else:
                day = calendar.monthrange(d.year, d.month)[1]
            try:
                d = date(d.year, d.month, day)
            except ValueError:
                pass

        elif txn_type == "Withdrawal" and random.random() < 0.4:
            # ATM withdrawals cluster Friday (4) or Saturday (5)
            days_ahead = (4 - d.weekday()) % 7
            d = d + timedelta(days=days_ahead)
            if d > end_date:
                d = d - timedelta(days=7)

        else:
            # 80% weekday bias
            if random.random() < 0.80:
                # Shift to nearest weekday if weekend
                while d.weekday() >= 5:
                    d -= timedelta(days=1)

        if start_date <= d <= end_date:
            break

    hour   = random.randint(8, 20)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime(d.year, d.month, d.day, hour, minute, second)

# ============================================================
# CUSTOMER META
# ============================================================
def build_customer_meta():
    meta = {}
    for i in range(1, NUM_CUSTOMERS + 1):
        branch_id = random.randint(1, 15)

        if i in SCENARIO_STUDENT:
            dob          = rand_date_between(date(1998, 1, 1), date(2003, 12, 31))
            credit_score = random.randint(300, 580)
        elif i in SCENARIO_FHSA:
            dob          = rand_date_between(date(1986, 1, 1), date(1999, 12, 31))
            credit_score = random.randint(650, 800)
        elif i in SCENARIO_HIGH_VALUE:
            dob          = rand_date_between(date(1963, 1, 1), date(1983, 12, 31))
            credit_score = random.randint(750, 900)
        elif i in SCENARIO_HIGH_CREDIT:
            dob          = rand_date_between(date(1960, 1, 1), date(1990, 12, 31))
            credit_score = random.randint(780, 900)
        elif i in SCENARIO_DEFAULTED:
            dob          = rand_date_between(date(1970, 1, 1), date(1995, 12, 31))
            credit_score = random.randint(300, 500)
        elif i in SCENARIO_IN_ARREARS:
            dob          = rand_date_between(date(1970, 1, 1), date(1995, 12, 31))
            credit_score = random.randint(450, 620)
        else:
            dob          = rand_date_between(date(1955, 1, 1), date(2000, 12, 31))
            credit_score = random.randint(580, 850)

        min_join   = max(add_months(dob, 18 * 12), BRANCH_OPENED[branch_id], date(2015, 1, 1))
        max_join   = date(2023, 12, 31)
        if min_join > max_join:
            min_join = max_join
        created_at = rand_date_between(min_join, max_join)
        is_active  = 0 if i in SCENARIO_DORMANT else 1

        meta[i] = {
            "dob": dob, "created_at": created_at,
            "credit_score": credit_score, "branch_id": branch_id,
            "is_active": is_active,
        }
    return meta

# ============================================================
# BRANCHES
# ============================================================
def generate_branches():
    rows = []
    for bid, name, city, prov, postal, phone in BRANCHES:
        rows.append(
            f"({bid}, '{esc(name)}', '{esc(city)}', '{prov}', '{postal}', '{phone}', '{BRANCH_OPENED[bid]}')"
        )
    return rows

# ============================================================
# CUSTOMERS
# ============================================================
def generate_customers(meta):
    rows = []
    for i in range(1, NUM_CUSTOMERS + 1):
        m        = meta[i]
        province = random.choice(PROVINCES)
        city     = random.choice(PROVINCE_CITIES[province])
        first    = fake.first_name()
        last     = fake.last_name()
        email    = f"{first.lower()}.{last.lower()}.{i}@{random.choice(['gmail.com','yahoo.ca','outlook.com','hotmail.ca'])}"
        rows.append(
            f"({i}, '{esc(first)}', '{esc(last)}', '{esc(email)}', '{rand_phone()}', "
            f"'{m['dob']}', '{random.randint(1000,9999)}', '{esc(city)}', '{province}', "
            f"'{rand_postal()}', {m['credit_score']}, {m['is_active']}, "
            f"'{m['created_at']}', {m['branch_id']})"
        )
    return rows

# ============================================================
# ACCOUNTS
# ============================================================
def generate_accounts(meta):
    rows              = []
    account_id        = 1
    customer_accounts = {}

    for cid in range(1, NUM_CUSTOMERS + 1):
        customer_accounts[cid] = []
        m   = meta[cid]
        age = (TODAY - m['dob']).days // 365

        if cid in SCENARIO_MULTI_ACCOUNT:
            types = ["Chequing", "TFSA", "RRSP"]
        elif cid in SCENARIO_FHSA:
            types = ["FHSA", "Chequing"]
        elif cid in SCENARIO_DORMANT:
            types = ["Chequing"]
        elif cid in SCENARIO_STUDENT:
            types = random.choice([["Chequing"], ["Chequing", "Savings"]])
        else:
            eligible = ["Chequing", "Savings"]
            if age >= 18: eligible.append("TFSA")
            if age >= 25: eligible.append("GIC")
            if age >= 30: eligible.append("RRSP")
            num   = random.choices([1, 2, 3], weights=[0.3, 0.45, 0.25])[0]
            num   = min(num, len(eligible))
            types = random.sample(eligible, num)
            if "Chequing" not in types:
                types[0] = "Chequing"

        for atype in types:
            branch_id   = m['branch_id']
            opened_date = rand_date_between(m['created_at'], date(2024, 6, 1))

            if cid in SCENARIO_FROZEN_ACCOUNT:
                status = "Frozen"
            elif cid in SCENARIO_DORMANT:
                status = "Active"
            elif random.random() < 0.04:
                status = "Closed"
            else:
                status = "Active"

            # Starting balance (will be updated after running transactions)
            if atype == "Chequing":
                balance = round(random.uniform(500 if cid not in SCENARIO_STUDENT else 50,
                                               80000 if cid in SCENARIO_HIGH_VALUE else 12000), 2)
            elif atype == "Savings":
                balance = round(random.uniform(500, 250000 if cid in SCENARIO_HIGH_VALUE else 50000), 2)
            elif atype == "TFSA":
                balance = round(random.uniform(1000, 75000), 2)
            elif atype == "RRSP":
                balance = round(random.uniform(5000, min(200000, age * 3000)), 2)
            elif atype == "FHSA":
                balance = round(random.uniform(1000, 40000), 2)
            elif atype == "GIC":
                balance = round(random.uniform(5000, 100000), 2)
            else:
                balance = round(random.uniform(200, 10000), 2)

            if cid in SCENARIO_DORMANT:
                balance = round(random.uniform(10, 300), 2)

            interest_rate = 0.00
            if atype == "Savings": interest_rate = round(random.uniform(1.5, 4.55), 2)
            elif atype == "TFSA":  interest_rate = round(random.uniform(2.0, 5.0), 2)
            elif atype == "RRSP":  interest_rate = round(random.uniform(2.0, 6.0), 2)
            elif atype == "GIC":   interest_rate = round(random.uniform(3.5, 5.55), 2)
            elif atype == "FHSA":  interest_rate = round(random.uniform(2.5, 5.0), 2)

            customer_accounts[cid].append({
                "account_id":   account_id,
                "account_type": atype,
                "balance":      balance,
                "opened_date":  opened_date,
                "status":       status,
                "branch_id":    branch_id,
                "interest_rate": interest_rate,
            })
            account_id += 1

    return customer_accounts

# ============================================================
# TRANSACTIONS — FIX 1 (running balance) + FIX 3 (weekday bias)
# + FIX 4 (RRSP withdrawals at 5%)
# ============================================================
def generate_transactions(customer_accounts, meta):
    """
    Generate transactions per account in chronological order.
    balance_after is computed as a true running balance.
    """
    # Step 1: Distribute NUM_TRANSACTIONS across active accounts
    active_accounts = []
    for cid, accs in customer_accounts.items():
        if cid in SCENARIO_DORMANT or cid in SCENARIO_FROZEN_ACCOUNT:
            continue
        for acc in accs:
            if acc["status"] in ("Frozen", "Closed"):
                continue
            if not VALID_TXN_TYPES.get(acc["account_type"]):
                continue  # GIC
            active_accounts.append((cid, acc))

    # Step 2: Assign transaction counts per account (weighted by account type)
    account_txn_counts = {}
    weights = []
    for cid, acc in active_accounts:
        w = 5 if acc["account_type"] == "Chequing" else 2
        if cid in SCENARIO_ETRANSFER and acc["account_type"] == "Chequing":
            w = 10
        weights.append(w)

    total_weight = sum(weights)
    for idx, (cid, acc) in enumerate(active_accounts):
        count = max(1, round(NUM_TRANSACTIONS * weights[idx] / total_weight))
        account_txn_counts[acc["account_id"]] = count

    # Adjust to exactly NUM_TRANSACTIONS
    diff = sum(account_txn_counts.values()) - NUM_TRANSACTIONS
    keys = list(account_txn_counts.keys())
    for i in range(abs(diff)):
        k = keys[i % len(keys)]
        account_txn_counts[k] += (-1 if diff > 0 else 1)
        if account_txn_counts[k] < 1:
            account_txn_counts[k] = 1

    # Step 3: Generate transactions per account with running balance
    all_txns = []  # list of row strings

    for cid, acc in active_accounts:
        aid      = acc["account_id"]
        atype    = acc["account_type"]
        n        = account_txn_counts.get(aid, 0)
        if n == 0:
            continue

        valid_types = VALID_TXN_TYPES[atype]
        branch_id   = meta[cid]["branch_id"]
        open_dt     = acc["opened_date"]
        end_dt      = date(2025, 12, 31)

        # Generate n raw events (type, amount, date) then sort by date
        events = []
        for _ in range(n):
            # FIX 4: RRSP withdrawals at ~5% rate
            if atype == "RRSP":
                txn_type = random.choices(
                    ["Deposit", "Transfer", "Withdrawal"],
                    weights=[60, 35, 5]
                )[0]
            elif atype == "Chequing" and cid in SCENARIO_ETRANSFER:
                txn_type = random.choices(
                    valid_types,
                    weights=[15, 10, 15, 10, 50]
                )[0]
            else:
                txn_type = random.choice(valid_types)

            # FIX 3: Realistic datetime with weekday/payroll bias
            txn_date = realistic_txn_datetime(open_dt, end_dt, txn_type)

            if txn_type == "Deposit":
                amount = round(random.uniform(100, 8000), 2)
                if "Payroll" in random.choice(TXN_DESCRIPTIONS["Deposit"]):
                    amount = round(random.uniform(1500, 5000), 2)
                desc = random.choice(TXN_DESCRIPTIONS["Deposit"])

            elif txn_type == "Withdrawal":
                if atype == "RRSP":
                    amount = round(random.uniform(2000, 35000), 2)
                    desc   = random.choice(TXN_DESCRIPTIONS["RRSP Withdrawal"])
                else:
                    amount = round(random.uniform(20, 1000), 2)
                    desc   = random.choice(TXN_DESCRIPTIONS["Withdrawal"])

            elif txn_type == "Transfer":
                amount = round(random.uniform(100, 5000), 2)
                desc   = random.choice(TXN_DESCRIPTIONS["Transfer"])

            elif txn_type == "Bill Payment":
                amount = round(random.uniform(40, 2500), 2)
                desc   = random.choice(TXN_DESCRIPTIONS["Bill Payment"])

            else:  # Interac e-Transfer
                amount = round(random.uniform(10, 2000), 2)
                desc   = f"Interac e-Transfer sent to {esc(fake.first_name() + ' ' + fake.last_name())}"

            events.append((txn_date, txn_type, amount, desc))

        # Sort events chronologically — this is FIX 1
        events.sort(key=lambda x: x[0])

        # Compute running balance starting from account's opening balance
        running_balance = acc["balance"]

        for txn_date, txn_type, amount, desc in events:
            if txn_type in ("Deposit",):
                running_balance = round(running_balance + amount, 2)
            else:
                running_balance = round(max(0.01, running_balance - amount), 2)

            balance_after = running_balance

            all_txns.append(
                f"(NULL, {aid}, {branch_id}, '{txn_type}', "
                f"{amount}, {balance_after}, '{txn_date}', '{esc(desc)}')"
            )

        # Update the account's current balance to final running balance
        acc["balance"] = running_balance

    return all_txns

# ============================================================
# ACCOUNTS SQL ROWS (built after transactions update balances)
# ============================================================
def build_account_rows(customer_accounts):
    rows = []
    for cid, accs in customer_accounts.items():
        for acc in accs:
            rows.append(
                f"({acc['account_id']}, {cid}, {acc['branch_id']}, "
                f"'{acc['account_type']}', {acc['balance']}, "
                f"{acc['interest_rate']}, '{acc['opened_date']}', '{acc['status']}')"
            )
    return rows

# ============================================================
# LOANS — FIX 2: allow multiple loans per customer
# ============================================================
def generate_loans(customer_accounts, meta):
    rows      = []
    loan_data = []
    loan_id   = 1
    has_mortgage = set()

    must_have  = list(SCENARIO_DEFAULTED) + list(SCENARIO_IN_ARREARS) + \
                 list(SCENARIO_PAID_OFF)  + list(SCENARIO_HIGH_VALUE)
    excluded   = set(SCENARIO_NO_LOAN) | set(SCENARIO_DORMANT) | set(SCENARIO_FHSA)
    eligible   = [c for c in range(1, NUM_CUSTOMERS + 1) if c not in excluded]
    other_pool = [c for c in eligible if c not in must_have]
    slots      = max(0, NUM_LOANS - len(must_have))
    others     = random.sample(other_pool, min(slots, len(other_pool)))
    primary    = must_have + others
    random.shuffle(primary)

    def add_loan(cid, loan_type_override=None):
        nonlocal loan_id
        m            = meta[cid]
        credit_score = m["credit_score"]
        branch_id    = m["branch_id"] if m["branch_id"] != 15 else random.randint(1, 14)

        if cid in SCENARIO_HIGH_VALUE:
            loan_type     = "Mortgage"
            principal     = round(random.uniform(700000, 1200000), 2)
            interest_rate = round(random.uniform(4.5, 6.5), 2)
            term_months   = 300
            has_mortgage.add(cid)
        elif cid in SCENARIO_STUDENT:
            loan_type     = "Student"
            principal     = round(random.uniform(10000, 60000), 2)
            interest_rate = round(random.uniform(5.0, 8.0), 2)
            term_months   = random.choice([60, 120])
        else:
            eligible_loans = ["Personal"]
            if credit_score >= 550: eligible_loans.append("Auto")
            if credit_score >= 620: eligible_loans += ["Mortgage"]
            if credit_score >= 620 and cid in has_mortgage: eligible_loans.append("HELOC")
            if credit_score >= 500: eligible_loans.append("Student")

            loan_type = loan_type_override or random.choice(eligible_loans)

            if loan_type == "Mortgage":
                principal     = round(random.uniform(200000, 900000), 2)
                term_months   = random.choice([240, 300, 360])
                interest_rate = round(random.uniform(4.0, 7.5), 2)
                has_mortgage.add(cid)
            elif loan_type == "HELOC":
                principal     = round(random.uniform(50000, 300000), 2)
                term_months   = random.choice([60, 120, 180])
                interest_rate = round(random.uniform(6.2, 8.5), 2)
            elif loan_type == "Auto":
                principal     = round(random.uniform(15000, 80000), 2)
                term_months   = random.choice([48, 60, 72, 84])
                interest_rate = round(random.uniform(5.5, 9.9), 2)
            elif loan_type == "Personal":
                principal     = round(random.uniform(3000, 50000), 2)
                term_months   = random.choice([24, 36, 48, 60])
                interest_rate = round(random.uniform(7.0, 14.9), 2)
            else:
                principal     = round(random.uniform(10000, 60000), 2)
                term_months   = random.choice([60, 120])
                interest_rate = round(random.uniform(5.0, 8.0), 2)

        monthly_payment = calc_monthly_payment(principal, interest_rate, term_months)
        start_date      = rand_date_between(date(2019, 1, 1), date(2023, 12, 31))
        end_date        = add_months(start_date, term_months)

        if cid in SCENARIO_DEFAULTED:   status = "Defaulted"
        elif cid in SCENARIO_IN_ARREARS: status = "In Arrears"
        elif cid in SCENARIO_PAID_OFF:   status = "Paid Off"
        elif end_date < TODAY:           status = "Paid Off"
        else:                            status = "Active"

        rows.append(
            f"({loan_id}, {cid}, {branch_id}, '{loan_type}', {principal}, "
            f"{interest_rate}, {term_months}, {monthly_payment}, "
            f"'{start_date}', '{end_date}', '{status}')"
        )
        loan_data.append({
            "loan_id": loan_id, "cid": cid, "principal": principal,
            "interest_rate": interest_rate, "term_months": term_months,
            "monthly_payment": monthly_payment, "start_date": start_date,
            "end_date": end_date, "status": status,
        })
        loan_id += 1

    # Primary loans
    for cid in primary:
        add_loan(cid)

    # FIX 2: ~20% of mortgage holders also get an auto loan
    mortgage_holders = [c for c in primary if c in has_mortgage
                        and c not in SCENARIO_DEFAULTED
                        and c not in SCENARIO_IN_ARREARS]
    second_loan_cids = random.sample(mortgage_holders, min(30, len(mortgage_holders)))
    for cid in second_loan_cids:
        add_loan(cid, loan_type_override="Auto")

    return rows, loan_data

# ============================================================
# CARDS
# ============================================================
def generate_cards(customer_accounts, meta):
    rows    = []
    card_id = 1
    sampled = random.sample(list(customer_accounts.keys()), min(NUM_CARDS, NUM_CUSTOMERS))

    for cid in sampled:
        accs          = customer_accounts[cid]
        chequing_accs = [a for a in accs if a["account_type"] == "Chequing"]
        if not chequing_accs:
            continue

        acc       = random.choice(chequing_accs)
        card_type = random.choice(["Debit", "Credit"])
        masked    = "*" * 12 + str(random.randint(1000, 9999))
        expiry    = add_months(acc["opened_date"], random.randint(24, 60))
        if expiry < date(2023, 1, 1):
            expiry = rand_date_between(date(2023, 1, 1), date(2028, 12, 31))

        credit_limit = None
        if card_type == "Credit":
            cs = meta[cid]["credit_score"]
            if cs < 600:   credit_limit = round(random.uniform(500, 2000), 2)
            elif cs < 700: credit_limit = round(random.uniform(2000, 8000), 2)
            elif cs < 800: credit_limit = round(random.uniform(5000, 15000), 2)
            else:          credit_limit = round(random.uniform(10000, 25000), 2)

        if cid in SCENARIO_BLOCKED_CARD: status = "Blocked"
        elif expiry < TODAY:             status = "Expired"
        elif random.random() < 0.04:     status = "Cancelled"
        else:                            status = "Active"

        credit_val = credit_limit if credit_limit is not None else "NULL"
        rows.append(
            f"({card_id}, {acc['account_id']}, {cid}, '{card_type}', '{masked}', "
            f"{credit_val}, '{expiry}', '{status}')"
        )
        card_id += 1

    return rows

# ============================================================
# LOAN PAYMENTS
# ============================================================
def generate_loan_payments(loan_data):
    rows       = []
    payment_id = 1

    for loan in loan_data:
        cid             = loan["cid"]
        loan_id         = loan["loan_id"]
        monthly_payment = loan["monthly_payment"]
        monthly_rate    = loan["interest_rate"] / 100 / 12
        start_date      = loan["start_date"]
        remaining       = loan["principal"]
        term_months     = loan["term_months"]

        if cid in SCENARIO_PAID_OFF:      num_payments = term_months
        elif cid in SCENARIO_DEFAULTED:   num_payments = random.randint(1, 4)
        elif cid in SCENARIO_IN_ARREARS:  num_payments = random.randint(3, 8)
        else:
            elapsed      = months_between(start_date, TODAY)
            num_payments = min(elapsed, term_months)

        payment_date = add_months(date(start_date.year, start_date.month, 1), 1)

        for _ in range(num_payments):
            if remaining <= 0.01:
                break
            if payment_date > TODAY and cid not in SCENARIO_PAID_OFF:
                break

            interest_portion  = round(remaining * monthly_rate, 2)
            principal_portion = round(monthly_payment - interest_portion, 2)
            if principal_portion <= 0:
                principal_portion = round(monthly_payment * 0.05, 2)
                interest_portion  = round(monthly_payment - principal_portion, 2)

            remaining = max(0.00, round(remaining - principal_portion, 2))
            rows.append(
                f"({payment_id}, {loan_id}, '{payment_date}', "
                f"{monthly_payment}, {principal_portion}, {interest_portion}, {remaining})"
            )
            payment_id  += 1
            payment_date = add_months(payment_date, 1)

    return rows

# ============================================================
# WRITE SQL
# ============================================================
def write_sql(filename):
    print("Generating data...")

    meta              = build_customer_meta()
    branch_rows       = generate_branches()
    customer_rows     = generate_customers(meta)
    customer_accounts = generate_accounts(meta)

    # Transactions update account balances in-place (running balance fix)
    txn_rows     = generate_transactions(customer_accounts, meta)
    account_rows = build_account_rows(customer_accounts)

    loan_rows, loan_data = generate_loans(customer_accounts, meta)
    card_rows            = generate_cards(customer_accounts, meta)
    payment_rows         = generate_loan_payments(loan_data)

    def write_inserts(f, table, columns, rows, chunk=500):
        f.write(f"-- {table.upper()}\n")
        for i in range(0, len(rows), chunk):
            batch = rows[i:i + chunk]
            f.write(f"INSERT INTO {table} ({columns}) VALUES\n")
            f.write(",\n".join(batch))
            f.write(";\n\n")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("-- =============================================================\n")
        f.write("-- BankCore SQL Project - TD Canada Trust\n")
        f.write("-- File: 02_insert_data.sql\n")
        f.write(f"-- Generated: {TODAY}\n")
        f.write("-- =============================================================\n\n")
        f.write("USE bankcore;\nSET FOREIGN_KEY_CHECKS = 0;\n\n")

        write_inserts(f, "branches",
            "branch_id, branch_name, city, province, postal_code, phone, opened_date",
            branch_rows)
        write_inserts(f, "customers",
            "customer_id, first_name, last_name, email, phone, date_of_birth, "
            "sin_last4, city, province, postal_code, credit_score, is_active, created_at, branch_id",
            customer_rows)
        write_inserts(f, "accounts",
            "account_id, customer_id, branch_id, account_type, balance, "
            "interest_rate, opened_date, status",
            account_rows)
        write_inserts(f, "transactions",
            "transaction_id, account_id, branch_id, transaction_type, amount, "
            "balance_after, transaction_date, description",
            txn_rows)
        write_inserts(f, "loans",
            "loan_id, customer_id, branch_id, loan_type, principal_amount, "
            "interest_rate, term_months, monthly_payment, start_date, end_date, status",
            loan_rows)
        write_inserts(f, "cards",
            "card_id, account_id, customer_id, card_type, card_number_masked, "
            "credit_limit, expiry_date, status",
            card_rows)
        write_inserts(f, "loan_payments",
            "payment_id, loan_id, payment_date, amount_paid, principal_portion, "
            "interest_portion, remaining_balance",
            payment_rows)

        f.write("SET FOREIGN_KEY_CHECKS = 1;\n")

    print(f"Done!")
    print(f"  Branches:      {len(branch_rows)}")
    print(f"  Customers:     {len(customer_rows)}")
    print(f"  Accounts:      {len(account_rows)}")
    print(f"  Transactions:  {len(txn_rows)}")
    print(f"  Loans:         {len(loan_rows)}")
    print(f"  Cards:         {len(card_rows)}")
    print(f"  Loan Payments: {len(payment_rows)}")

if __name__ == "__main__":
    write_sql(OUTPUT_FILE)
