# =============================================================================
# UTILS — PII hashing, ID generation, fake data helpers
# =============================================================================
import hashlib
import uuid
import random
import string
from faker import Faker

fake = Faker("en_US")
Faker.seed(42)
random.seed(42)

# -----------------------------------------------------------------------------
# ID GENERATORS
# -----------------------------------------------------------------------------
def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12].upper()}"

# -----------------------------------------------------------------------------
# PII HANDLING — per agreed GDPR/CCPA policy
# -----------------------------------------------------------------------------
def sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()

def hash_ssn_last4() -> str:
    last4 = str(random.randint(1000, 9999))
    return sha256(last4)

def hash_dob(dob: str) -> str:
    return sha256(dob)

def hash_email(email: str) -> str:
    return sha256(email)

def normalize_phone(phone: str) -> str:
    digits = "".join(c for c in phone if c.isdigit())
    if len(digits) == 10:
        return f"+1{digits}"
    return f"+{digits}"

def dob_year_only(dob: str) -> int:
    return int(dob[:4])

# -----------------------------------------------------------------------------
# FAKE DATA GENERATORS
# -----------------------------------------------------------------------------
def fake_person_data():
    dob = fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat()
    phone_raw = fake.numerify("##########")
    email_raw = fake.email()
    return {
        "full_name":  fake.name(),
        "dob_year":   dob_year_only(dob),
        "dob_hash":   hash_dob(dob),
        "ssn_hash":   hash_ssn_last4(),
        "phone":      normalize_phone(phone_raw),
        "email_hash": hash_email(email_raw),
        "gender":     random.choice(["M", "F", "NB"]),
    }

def fake_address(zip4=None):
    from config import HARTFORD_ZIPS, ALL_ZIPS
    z = zip4 or random.choice(ALL_ZIPS)
    suffix = str(random.randint(1000, 9999))
    return {
        "address_id": new_id("ADDR"),
        "zip4":       f"{z}-{suffix}",
        "city":       fake.city(),
        "state":      fake.state_abbr(),
        "country":    "US",
        "created_at": fake.date_this_decade().isoformat(),
    }

def fake_npi() -> str:
    return fake.numerify("##########")

def fake_bar_id() -> str:
    return fake.bothify("??######").upper()

def fake_ein() -> str:
    return fake.numerify("##-#######")

def fake_vin() -> str:
    chars = string.ascii_uppercase.replace("I", "").replace("O", "").replace("Q", "")
    return "".join(random.choices(chars + string.digits, k=17))

def fake_amount(low=500, high=250000) -> float:
    return round(random.uniform(low, high), 2)

def fake_reserve(amount: float) -> float:
    return round(amount * random.uniform(1.0, 2.5), 2)
