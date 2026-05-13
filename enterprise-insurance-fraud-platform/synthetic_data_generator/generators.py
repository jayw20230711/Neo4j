# =============================================================================
# GENERATORS — All 24 node labels
# Each function returns a list of dicts ready for MERGE into Neo4j
# =============================================================================
import random
from faker import Faker
from config import *
from utils import *

fake = Faker("en_US")

# -----------------------------------------------------------------------------
# FRAUD RINGS (20)
# -----------------------------------------------------------------------------
def gen_fraud_rings():
    rings = []
    for r in FRAUD_RING_DEFS:
        rings.append({
            "ring_id":        r["ring_id"],
            "component_id":   r["component_id"],
            "ring_type":      r["ring_type"],
            "lob":            r["lob"],
            "estimated_size": r["size"],
            "confirmed":      random.random() > 0.3,
            "detected_date":  date_str(random_date()),
            "status":         random.choice(["ACTIVE", "DISMANTLED", "UNDER_INVESTIGATION"]),
            "estimated_loss": fake_amount(50000, 5000000),
        })
    return rings

# -----------------------------------------------------------------------------
# PERSONS (8,000)
# -----------------------------------------------------------------------------
def gen_persons(n=8000):
    persons = []
    for _ in range(n):
        p = fake_person_data()
        p["person_id"] = new_id("PER")
        p["source_system"] = random.choice(list(SOURCE_SYSTEMS.keys()))
        p["created_at"] = date_str(random_date())
        p["pagerank"] = round(random.uniform(0.1, 10.0), 4)
        p["louvain_community"] = random.randint(0, 199)
        p["component_id"] = random.randint(0, 999)
        persons.append(p)
    return persons

# -----------------------------------------------------------------------------
# EMPLOYEES (3,000) — subset of persons
# -----------------------------------------------------------------------------
def gen_employees(person_ids, n=3000):
    sampled = random.sample(person_ids, min(n, len(person_ids)))
    employees = []
    for pid in sampled:
        employees.append({
            "employee_id":   new_id("EMP"),
            "person_id":     pid,
            "hire_date":     date_str(random_date(START_DATE, datetime(2023, 1, 1))),
            "department":    random.choice(["CLAIMS", "UNDERWRITING", "FINANCE", "OPS", "IT", "HR", "SALES"]),
            "job_title":     fake.job(),
            "status":        random.choice(["ACTIVE", "TERMINATED", "ON_LEAVE"]),
            "source_system": "WORKDAY",
        })
    return employees

# -----------------------------------------------------------------------------
# DEPENDENTS (2,000)
# -----------------------------------------------------------------------------
def gen_dependents(person_ids, n=2000):
    sampled = random.sample(person_ids, min(n, len(person_ids)))
    deps = []
    for pid in sampled:
        p = fake_person_data()
        deps.append({
            "dependent_id":  new_id("DEP"),
            "person_id":     pid,
            "relationship":  random.choice(["SPOUSE", "CHILD", "DOMESTIC_PARTNER"]),
            "full_name":     p["full_name"],
            "dob_year":      p["dob_year"],
            "dob_hash":      p["dob_hash"],
            "eligible":      random.random() > 0.05,
            "enrolled_date": date_str(random_date()),
        })
    return deps

# -----------------------------------------------------------------------------
# EMPLOYERS (500)
# -----------------------------------------------------------------------------
def gen_employers(n=500):
    employers = []
    for _ in range(n):
        employers.append({
            "employer_id":   new_id("EMPR"),
            "company_name":  fake.company(),
            "ein_hash":      sha256(fake_ein()),
            "industry":      fake.bs().split()[0].upper(),
            "zip4":          f"{random.choice(ALL_ZIPS)}-{random.randint(1000,9999)}",
            "state":         random.choices(STATES, STATE_WEIGHTS)[0],
            "employee_count":random.randint(10, 5000),
            "source_system": "SAP",
            "created_at":    date_str(random_date()),
        })
    return employers

# -----------------------------------------------------------------------------
# POLICIES (4,000)
# -----------------------------------------------------------------------------
def gen_policies(n=4000):
    policies = []
    for _ in range(n):
        lob = random.choices(ALL_LOBS, LOB_WEIGHTS)[0]
        eff = random_date(START_DATE, datetime(2024, 6, 1))
        exp = eff + timedelta(days=random.choice([365, 730, 1095]))
        policies.append({
            "policy_id":      new_id("POL"),
            "lob":            lob,
            "carrier":        random.choice(CARRIERS),
            "state":          random.choices(STATES, STATE_WEIGHTS)[0],
            "effective_date": date_str(eff),
            "expiry_date":    date_str(exp),
            "premium":        fake_amount(500, 50000),
            "status":         random.choice(["ACTIVE", "EXPIRED", "CANCELLED", "LAPSED"]),
            "source_system":  random.choice(["GUIDEWIRE", "DUCK_CREEK"]),
            "created_at":     date_str(eff),
        })
    return policies

# -----------------------------------------------------------------------------
# CLAIMS (5,000)
# -----------------------------------------------------------------------------
def gen_claims(policy_ids, n=5000):
    claims = []
    for _ in range(n):
        loss_dt = random_date()
        report_dt = loss_dt + timedelta(days=random.randint(0, 30))
        amount = fake_amount(1000, 500000)
        claims.append({
            "claim_id":       new_id("CLM"),
            "policy_id":      random.choice(policy_ids),
            "lob":            random.choices(ALL_LOBS, LOB_WEIGHTS)[0],
            "status":         random.choices(CLAIM_STATUSES, CLAIM_STATUS_WEIGHTS)[0],
            "loss_date":      date_str(loss_dt),
            "report_date":    date_str(report_dt),
            "claimed_amount": amount,
            "reserve_amount": fake_reserve(amount),
            "paid_amount":    round(amount * random.uniform(0, 1.1), 2),
            "fraud_score":    round(random.uniform(0, 100), 2),
            "source_system":  random.choice(["GUIDEWIRE", "DUCK_CREEK"]),
            "iso_flag":       random.random() > 0.85,
            "pagerank":       round(random.uniform(0.1, 10.0), 4),
            "louvain_community": random.randint(0, 199),
            "component_id":   random.randint(0, 999),
            "created_at":     date_str(report_dt),
        })
    return claims

# -----------------------------------------------------------------------------
# CLAIM VERSIONS (1 per claim — LOB-specific shape)
# -----------------------------------------------------------------------------
def gen_claim_versions(claim_ids):
    versions = []
    for cid in claim_ids:
        lob = random.choices(ALL_LOBS, LOB_WEIGHTS)[0]
        versions.append({
            "version_id":   new_id("VER"),
            "claim_id":     cid,
            "lob":          lob,
            "version_num":  1,
            "shape":        f"{lob.lower()}_version",
            "created_at":   date_str(random_date()),
            "created_by":   random.choice(list(SOURCE_SYSTEMS.keys())),
        })
    return versions

# -----------------------------------------------------------------------------
# COVERAGE LINES (3,000)
# -----------------------------------------------------------------------------
def gen_coverage_lines(policy_ids, n=3000):
    lines = []
    for _ in range(n):
        lines.append({
            "coverage_id":   new_id("COV"),
            "policy_id":     random.choice(policy_ids),
            "coverage_type": random.choice(["BI", "PD", "MED", "UM", "COMP", "COLL", "LIABILITY"]),
            "limit_amount":  fake_amount(25000, 2000000),
            "deductible":    random.choice([0, 500, 1000, 2500, 5000]),
            "lob":           random.choices(ALL_LOBS, LOB_WEIGHTS)[0],
            "active":        random.random() > 0.1,
        })
    return lines

# -----------------------------------------------------------------------------
# CLAIM PAYMENTS (4,000)
# -----------------------------------------------------------------------------
def gen_claim_payments(claim_ids, n=4000):
    payments = []
    for _ in range(n):
        pay_dt = random_date()
        payments.append({
            "payment_id":    new_id("PAY"),
            "claim_id":      random.choice(claim_ids),
            "payment_date":  date_str(pay_dt),
            "amount":        fake_amount(500, 100000),
            "payment_type":  random.choice(["INDEMNITY", "MEDICAL", "LEGAL", "EXPENSE", "SUPPLEMENT"]),
            "payee_type":    random.choice(["CLAIMANT", "PROVIDER", "ATTORNEY", "REPAIR_SHOP", "EMPLOYER"]),
            "check_number":  fake.numerify("########"),
            "status":        random.choice(["ISSUED", "CLEARED", "VOIDED", "HELD"]),
            "source_system": "SAP",
        })
    return payments

# -----------------------------------------------------------------------------
# MEDICAL PROVIDERS (500)
# -----------------------------------------------------------------------------
def gen_medical_providers(n=500):
    providers = []
    for _ in range(n):
        providers.append({
            "npi":           fake_npi(),
            "name":          fake.company() + " Medical",
            "specialty":     random.choice(MEDICAL_SPECIALTIES),
            "zip4":          f"{random.choice(ALL_ZIPS)}-{random.randint(1000,9999)}",
            "state":         random.choices(STATES, STATE_WEIGHTS)[0],
            "license_active":random.random() > 0.05,
            "iso_flagged":   random.random() > 0.90,
            "claim_count":   random.randint(1, 200),
            "pagerank":      round(random.uniform(0.1, 15.0), 4),
            "source_system": "TRIZETTO",
            "created_at":    date_str(random_date()),
        })
    return providers

# -----------------------------------------------------------------------------
# MEDICAL BILLS (3,000)
# -----------------------------------------------------------------------------
def gen_medical_bills(claim_ids, provider_npis, n=3000):
    bills = []
    for _ in range(n):
        billed = fake_amount(200, 50000)
        bills.append({
            "bill_id":       new_id("BILL"),
            "claim_id":      random.choice(claim_ids),
            "npi":           random.choice(provider_npis),
            "service_date":  date_str(random_date()),
            "cpt_code":      random.choice(CPT_CODES),
            "billed_amount": billed,
            "allowed_amount":round(billed * random.uniform(0.4, 1.0), 2),
            "paid_amount":   round(billed * random.uniform(0.3, 0.9), 2),
            "icd10_code":    fake.bothify("???##.#").upper(),
            "facility_flag": random.random() > 0.3,
            "source_system": "TRIZETTO",
        })
    return bills

# -----------------------------------------------------------------------------
# REPAIR SHOPS (200)
# -----------------------------------------------------------------------------
def gen_repair_shops(n=200):
    shops = []
    for _ in range(n):
        shops.append({
            "shop_id":       new_id("SHOP"),
            "name":          fake.company() + " Auto Repair",
            "zip4":          f"{random.choice(ALL_ZIPS)}-{random.randint(1000,9999)}",
            "state":         random.choices(STATES, STATE_WEIGHTS)[0],
            "license_num":   fake.bothify("??-######").upper(),
            "iso_flagged":   random.random() > 0.90,
            "avg_estimate":  fake_amount(500, 15000),
            "source_system": "GUIDEWIRE",
            "created_at":    date_str(random_date()),
        })
    return shops

# -----------------------------------------------------------------------------
# ATTORNEYS (300)
# -----------------------------------------------------------------------------
def gen_attorneys(n=300):
    attorneys = []
    for _ in range(n):
        attorneys.append({
            "bar_id":        fake_bar_id(),
            "full_name":     fake.name(),
            "firm_name":     fake.company() + " Law",
            "state_bar":     random.choices(STATES, STATE_WEIGHTS)[0],
            "zip4":          f"{random.choice(ALL_ZIPS)}-{random.randint(1000,9999)}",
            "iso_flagged":   random.random() > 0.88,
            "claim_count":   random.randint(1, 150),
            "avg_settlement":fake_amount(5000, 200000),
            "source_system": "GUIDEWIRE",
            "created_at":    date_str(random_date()),
        })
    return attorneys

# -----------------------------------------------------------------------------
# TOW COMPANIES (100)
# -----------------------------------------------------------------------------
def gen_tow_companies(n=100):
    companies = []
    for _ in range(n):
        companies.append({
            "company_id":    new_id("TOW"),
            "name":          fake.company() + " Towing",
            "zip4":          f"{random.choice(ALL_ZIPS)}-{random.randint(1000,9999)}",
            "state":         random.choices(STATES, STATE_WEIGHTS)[0],
            "license_num":   fake.bothify("TOW-######").upper(),
            "iso_flagged":   random.random() > 0.92,
            "source_system": "GUIDEWIRE",
        })
    return companies

# -----------------------------------------------------------------------------
# ADJUSTERS (400)
# -----------------------------------------------------------------------------
def gen_adjusters(n=400):
    adjusters = []
    for _ in range(n):
        adjusters.append({
            "adjuster_id":   new_id("ADJ"),
            "full_name":     fake.name(),
            "territory":     random.choices(STATES, STATE_WEIGHTS)[0],
            "zip4":          f"{random.choice(ALL_ZIPS)}-{random.randint(1000,9999)}",
            "lob":           random.choices(ALL_LOBS, LOB_WEIGHTS)[0],
            "approval_rate": round(random.uniform(0.60, 0.99), 3),
            "claim_count":   random.randint(10, 500),
            "siu_referrals": random.randint(0, 50),
            "source_system": random.choice(["GUIDEWIRE", "DUCK_CREEK"]),
            "created_at":    date_str(random_date()),
        })
    return adjusters

# -----------------------------------------------------------------------------
# VEHICLES (2,000)
# -----------------------------------------------------------------------------
def gen_vehicles(n=2000):
    vehicles = []
    makes = ["Toyota", "Honda", "Ford", "Chevrolet", "BMW", "Mercedes", "Nissan", "Hyundai"]
    for _ in range(n):
        vehicles.append({
            "vin":           fake_vin(),
            "make":          random.choice(makes),
            "model":         fake.word().capitalize(),
            "year":          random.randint(2005, 2024),
            "state_reg":     random.choices(STATES, STATE_WEIGHTS)[0],
            "zip4":          f"{random.choice(ALL_ZIPS)}-{random.randint(1000,9999)}",
            "total_loss":    random.random() > 0.90,
            "source_system": random.choice(["GUIDEWIRE", "DUCK_CREEK"]),
            "created_at":    date_str(random_date()),
        })
    return vehicles

# -----------------------------------------------------------------------------
# FLEETS (50)
# -----------------------------------------------------------------------------
def gen_fleets(n=50):
    fleets = []
    for _ in range(n):
        fleets.append({
            "fleet_id":      new_id("FLT"),
            "name":          fake.company() + " Fleet",
            "vehicle_count": random.randint(5, 200),
            "state":         random.choices(STATES, STATE_WEIGHTS)[0],
            "zip4":          f"{random.choice(ALL_ZIPS)}-{random.randint(1000,9999)}",
            "source_system": "DUCK_CREEK",
        })
    return fleets

# -----------------------------------------------------------------------------
# ADDRESSES (6,000)
# -----------------------------------------------------------------------------
def gen_addresses(n=6000):
    return [fake_address() for _ in range(n)]

# -----------------------------------------------------------------------------
# PHONES (8,000) — stored normalized, not hashed (fraud signal)
# -----------------------------------------------------------------------------
def gen_phones(n=8000):
    phones = []
    for _ in range(n):
        raw = fake.numerify("##########")
        normed = normalize_phone(raw)
        phones.append({
            "phone_hash": sha256(normed),   # unique key
            "phone":      normed,            # stored per policy
            "carrier":    random.choice(["AT&T", "Verizon", "T-Mobile", "Sprint", "Unknown"]),
            "type":       random.choice(["MOBILE", "LANDLINE", "VOIP"]),
            "created_at": date_str(random_date()),
        })
    return phones

# -----------------------------------------------------------------------------
# BANK ACCOUNTS (2,000)
# -----------------------------------------------------------------------------
def gen_bank_accounts(n=2000):
    accounts = []
    for _ in range(n):
        accounts.append({
            "account_id":   new_id("BANK"),
            "last4":        str(random.randint(1000, 9999)),
            "bank_name":    random.choice(["Chase", "BofA", "Wells Fargo", "Citizens", "Webster", "TD Bank"]),
            "account_type": random.choice(["CHECKING", "SAVINGS"]),
            "state":        random.choices(STATES, STATE_WEIGHTS)[0],
            "created_at":   date_str(random_date()),
        })
    return accounts

# -----------------------------------------------------------------------------
# CROSS SYSTEM IDs (2,000) — entity resolution links
# -----------------------------------------------------------------------------
def gen_cross_system_ids(person_ids, n=2000):
    sampled = random.sample(person_ids, min(n, len(person_ids)))
    xrefs = []
    for pid in sampled:
        for sys in random.sample(list(SOURCE_SYSTEMS.keys()), random.randint(1, 3)):
            xrefs.append({
                "xref_id":       new_id("XRF"),
                "person_id":     pid,
                "source_system": sys,
                "external_id":   fake.numerify("########"),
                "match_score":   round(random.uniform(0.75, 1.0), 3),
                "created_at":    date_str(random_date()),
            })
    return xrefs

# -----------------------------------------------------------------------------
# LITIGATION EVENTS (500)
# -----------------------------------------------------------------------------
def gen_litigation_events(claim_ids, n=500):
    events = []
    for _ in range(n):
        filed = random_date()
        events.append({
            "litigation_id": new_id("LIT"),
            "claim_id":      random.choice(claim_ids),
            "filed_date":    date_str(filed),
            "court":         random.choice(["CT Superior", "NY Supreme", "NJ Superior", "MA Superior", "Federal"]),
            "case_number":   fake.bothify("??-##-#####").upper(),
            "status":        random.choice(["FILED", "DISCOVERY", "TRIAL", "SETTLED", "DISMISSED"]),
            "demand_amount": fake_amount(10000, 2000000),
            "settle_amount": fake_amount(5000, 1500000),
            "source_system": "GUIDEWIRE",
        })
    return events

# -----------------------------------------------------------------------------
# INJURY RECORDS (2,000)
# -----------------------------------------------------------------------------
def gen_injury_records(claim_ids, n=2000):
    records = []
    for _ in range(n):
        records.append({
            "injury_id":    new_id("INJ"),
            "claim_id":     random.choice(claim_ids),
            "injury_type":  random.choice(INJURY_TYPES),
            "body_part":    random.choice(["BACK", "NECK", "KNEE", "SHOULDER", "WRIST", "HEAD", "HIP", "ANKLE"]),
            "severity":     random.choice(["MINOR", "MODERATE", "SEVERE", "PERMANENT", "FATAL"]),
            "treatment_start": date_str(random_date()),
            "icd10":        fake.bothify("???##.#").upper(),
            "source_system":random.choice(["GUIDEWIRE", "TRIZETTO"]),
        })
    return records
