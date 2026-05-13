# =============================================================================
# CONFIG — Hartford CT Geography, LOBs, Fraud Patterns
# =============================================================================
import random
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# GEOGRAPHY — Hartford CT + surrounding no-fault states
# -----------------------------------------------------------------------------
HARTFORD_ZIPS = [
    "06101", "06102", "06103", "06104", "06105",
    "06106", "06107", "06108", "06109", "06110",
    "06111", "06112", "06114", "06115", "06117",
    "06118", "06119", "06120", "06160", "06167",
]
SURROUNDING_ZIPS = [
    # West Hartford, Wethersfield, Glastonbury, East Hartford, Manchester
    "06107", "06119", "06109", "06108", "06040",
    # Bridgeport, New Haven, Stamford
    "06604", "06510", "06901",
    # Springfield MA, Providence RI
    "01101", "02901",
]
ALL_ZIPS = HARTFORD_ZIPS + SURROUNDING_ZIPS

STATES = ["CT", "NY", "NJ", "MA"]
STATE_WEIGHTS = [0.60, 0.20, 0.12, 0.08]

CARRIERS = ["Travelers", "Aetna", "The Hartford", "Cigna Re", "Liberty Mutual"]

# -----------------------------------------------------------------------------
# SOURCE SYSTEMS (Layer 1)
# -----------------------------------------------------------------------------
SOURCE_SYSTEMS = {
    "GUIDEWIRE":   "Guidewire Claims Center",
    "DUCK_CREEK":  "Duck Creek Policy",
    "TRIZETTO":    "TriZetto Medical Billing",
    "SAP":         "SAP Finance",
    "SALESFORCE":  "Salesforce CRM",
}

# -----------------------------------------------------------------------------
# LOBs PER GROUP
# -----------------------------------------------------------------------------
LOB_GROUP1_PC = [
    "PROPERTY", "LIABILITY", "FLEET_AUTO", "UMBRELLA",
    "FLOOD", "CYBER", "EPL", "DO", "PROF_LIABILITY",
]
LOB_GROUP2_WC = ["WORKERS_COMP"]
LOB_GROUP3_BENEFITS = ["KEY_PERSON_LIFE", "DISABILITY", "HRA_HSA", "EMPLOYEE_BENEFITS"]

ALL_LOBS = LOB_GROUP1_PC + LOB_GROUP2_WC + LOB_GROUP3_BENEFITS

LOB_WEIGHTS = [
    0.18, 0.15, 0.12, 0.05,   # P&C heavy
    0.05, 0.04, 0.04, 0.03, 0.04,
    0.12,                       # WC
    0.04, 0.06, 0.04, 0.04,    # Benefits
]

# -----------------------------------------------------------------------------
# DATE RANGE — 10 years of claims
# -----------------------------------------------------------------------------
START_DATE = datetime(2015, 1, 1)
END_DATE   = datetime(2024, 12, 31)

def random_date(start=START_DATE, end=END_DATE):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def date_str(dt):
    return dt.strftime("%Y-%m-%d")

# -----------------------------------------------------------------------------
# FRAUD RINGS — 20 rings with component IDs
# -----------------------------------------------------------------------------
FRAUD_RING_DEFS = [
    {"ring_id": f"RING_{i:03d}", "component_id": i,
     "ring_type": rt, "lob": lob, "size": sz}
    for i, (rt, lob, sz) in enumerate([
        ("MEDICAL_MILL",        "LIABILITY",         45),
        ("MEDICAL_MILL",        "WORKERS_COMP",      38),
        ("STAGED_ACCIDENT",     "FLEET_AUTO",        22),
        ("STAGED_ACCIDENT",     "LIABILITY",         18),
        ("ARSON_RING",          "PROPERTY",          12),
        ("ARSON_RING",          "FLOOD",             10),
        ("PHANTOM_EMPLOYEE",    "EMPLOYEE_BENEFITS", 30),
        ("PHANTOM_EMPLOYEE",    "WORKERS_COMP",      25),
        ("ADJUSTER_COLLUSION",  "LIABILITY",         15),
        ("ADJUSTER_COLLUSION",  "WORKERS_COMP",      20),
        ("ATTORNEY_PIPELINE",   "LIABILITY",         35),
        ("ATTORNEY_PIPELINE",   "WORKERS_COMP",      28),
        ("SYNTHETIC_ID",        "LIABILITY",         20),
        ("SYNTHETIC_ID",        "EMPLOYEE_BENEFITS", 18),
        ("CROSS_CARRIER",       "LIABILITY",         40),
        ("CROSS_CARRIER",       "WORKERS_COMP",      32),
        ("CONTRACTOR_COLLUDE",  "PROPERTY",          16),
        ("CONTRACTOR_COLLUDE",  "FLOOD",             14),
        ("PHANTOM_PASSENGER",   "FLEET_AUTO",        22),
        ("DISABILITY_FRAUD",    "DISABILITY",        20),
    ])
]

# -----------------------------------------------------------------------------
# CLAIM STATUS DISTRIBUTION
# -----------------------------------------------------------------------------
CLAIM_STATUSES = ["OPEN", "CLOSED", "PENDING_SIU", "PAYMENT_HOLD", "LITIGATED", "DENIED"]
CLAIM_STATUS_WEIGHTS = [0.35, 0.40, 0.08, 0.07, 0.06, 0.04]

# -----------------------------------------------------------------------------
# INJURY TYPES (WC + Liability)
# -----------------------------------------------------------------------------
INJURY_TYPES = [
    "SOFT_TISSUE", "FRACTURE", "LACERATION", "BURN",
    "REPETITIVE_STRESS", "BACK_INJURY", "HEAD_TRAUMA",
    "PSYCHOLOGICAL", "PERMANENT_DISABILITY", "FATALITY",
]

# -----------------------------------------------------------------------------
# CPT CODE POOL (medical billing)
# -----------------------------------------------------------------------------
CPT_CODES = [
    "99213", "99214", "99215",   # office visits
    "97110", "97012", "97035",   # physical therapy
    "72148", "72141", "73721",   # MRI
    "27447", "23472", "22612",   # surgical
    "99281", "99282", "99283",   # ER visits
    "20610", "20600", "64483",   # injections
]

# -----------------------------------------------------------------------------
# SPECIALTY POOL
# -----------------------------------------------------------------------------
MEDICAL_SPECIALTIES = [
    "ORTHOPEDICS", "NEUROLOGY", "PAIN_MANAGEMENT",
    "EMERGENCY_MEDICINE", "RADIOLOGY", "PHYSICAL_THERAPY",
    "CHIROPRACTIC", "PSYCHIATRY", "GENERAL_SURGERY",
]
