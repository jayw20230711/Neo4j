# =============================================================================
# MAIN — Orchestrates generation and loading of all 24 node labels
# =============================================================================
import os
import random
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

from generators import (
    gen_fraud_rings, gen_persons, gen_employees, gen_dependents,
    gen_employers, gen_policies, gen_claims, gen_claim_versions,
    gen_coverage_lines, gen_claim_payments, gen_medical_providers,
    gen_medical_bills, gen_repair_shops, gen_attorneys, gen_tow_companies,
    gen_adjusters, gen_vehicles, gen_fleets, gen_addresses, gen_phones,
    gen_bank_accounts, gen_cross_system_ids, gen_litigation_events,
    gen_injury_records,
)
from loader import load_nodes, load_relationships, verify, get_driver

# -----------------------------------------------------------------------------
# GENERATE ALL NODES
# -----------------------------------------------------------------------------
print("=== GENERATING NODES ===")

fraud_rings      = gen_fraud_rings()
persons          = gen_persons(8000)
employers        = gen_employers(500)
policies         = gen_policies(4000)
claims           = gen_claims([p["policy_id"] for p in policies], 5000)
adjusters        = gen_adjusters(400)
medical_providers= gen_medical_providers(500)
repair_shops     = gen_repair_shops(200)
attorneys        = gen_attorneys(300)
tow_companies    = gen_tow_companies(100)
vehicles         = gen_vehicles(2000)
fleets           = gen_fleets(50)
addresses        = gen_addresses(6000)
phones           = gen_phones(8000)
bank_accounts    = gen_bank_accounts(2000)
employees        = gen_employees([p["person_id"] for p in persons], 3000)
dependents       = gen_dependents([p["person_id"] for p in persons], 2000)
coverage_lines   = gen_coverage_lines([p["policy_id"] for p in policies], 3000)
claim_versions   = gen_claim_versions([c["claim_id"] for c in claims])
claim_payments   = gen_claim_payments([c["claim_id"] for c in claims], 4000)
medical_bills    = gen_medical_bills(
                     [c["claim_id"] for c in claims],
                     [p["npi"] for p in medical_providers], 3000)
cross_system_ids = gen_cross_system_ids([p["person_id"] for p in persons], 2000)
litigation_events= gen_litigation_events([c["claim_id"] for c in claims], 500)
injury_records   = gen_injury_records([c["claim_id"] for c in claims], 2000)

node_data = {
    "FraudRing":       fraud_rings,
    "Person":          persons,
    "Employee":        employees,
    "Dependent":       dependents,
    "Employer":        employers,
    "Policy":          policies,
    "CoverageLine":    coverage_lines,
    "Claim":           claims,
    "ClaimVersion":    claim_versions,
    "ClaimPayment":    claim_payments,
    "MedicalProvider": medical_providers,
    "MedicalBill":     medical_bills,
    "RepairShop":      repair_shops,
    "Attorney":        attorneys,
    "TowCompany":      tow_companies,
    "Adjuster":        adjusters,
    "Vehicle":         vehicles,
    "Fleet":           fleets,
    "Address":         addresses,
    "Phone":           phones,
    "BankAccount":     bank_accounts,
    "CrossSystemID":   cross_system_ids,
    "LitigationEvent": litigation_events,
    "InjuryRecord":    injury_records,
}

total_nodes = sum(len(v) for v in node_data.values())
print(f"\nTotal nodes to load: {total_nodes:,}")

# -----------------------------------------------------------------------------
# BUILD RELATIONSHIPS
# -----------------------------------------------------------------------------
print("\n=== BUILDING RELATIONSHIPS ===")

person_ids   = [p["person_id"]   for p in persons]
claim_ids    = [c["claim_id"]    for c in claims]
policy_ids   = [p["policy_id"]   for p in policies]
adj_ids      = [a["adjuster_id"] for a in adjusters]
shop_ids     = [s["shop_id"]     for s in repair_shops]
npi_list     = [p["npi"]         for p in medical_providers]
bar_ids      = [a["bar_id"]      for a in attorneys]
address_ids  = [a["address_id"]  for a in addresses]
phone_hashes = [p["phone_hash"]  for p in phones]
account_ids  = [b["account_id"]  for b in bank_accounts]
employer_ids = [e["employer_id"] for e in employers]
fleet_ids    = [f["fleet_id"]    for f in fleets]
vins         = [v["vin"]         for v in vehicles]
ring_ids     = [r["ring_id"]     for r in fraud_rings]
xref_ids     = [x["xref_id"]     for x in cross_system_ids]

rel_data = {

    "CLAIM_UNDER_POLICY": [
        {"claim_id": c["claim_id"], "policy_id": c["policy_id"]}
        for c in claims
    ],

    "CLAIM_HAS_VERSION": [
        {"claim_id": v["claim_id"], "version_id": v["version_id"]}
        for v in claim_versions
    ],

    "CLAIM_HAS_PAYMENT": [
        {"claim_id": p["claim_id"], "payment_id": p["payment_id"]}
        for p in claim_payments
    ],

    "CLAIM_HAS_INJURY": [
        {"claim_id": i["claim_id"], "injury_id": i["injury_id"]}
        for i in injury_records
    ],

    "CLAIM_HAS_LITIGATION": [
        {"claim_id": l["claim_id"], "litigation_id": l["litigation_id"]}
        for l in litigation_events
    ],

    "CLAIM_FILED_BY": [
        {"claim_id": cid, "person_id": random.choice(person_ids)}
        for cid in claim_ids
    ],

    "CLAIM_HANDLED_BY": [
        {"claim_id": cid, "adjuster_id": random.choice(adj_ids)}
        for cid in claim_ids
    ],

    "CLAIM_INVOLVES_VEHICLE": [
        {"claim_id": cid, "vin": random.choice(vins)}
        for cid in random.sample(claim_ids, min(2000, len(claim_ids)))
    ],

    "CLAIM_INVOLVES_PROVIDER": [
        {"claim_id": cid, "npi": random.choice(npi_list)}
        for cid in random.sample(claim_ids, min(3000, len(claim_ids)))
    ],

    "CLAIM_REPRESENTED_BY": [
        {"claim_id": cid, "bar_id": random.choice(bar_ids)}
        for cid in random.sample(claim_ids, min(1000, len(claim_ids)))
    ],

    "CLAIM_REPAIRED_BY": [
        {"claim_id": cid, "shop_id": random.choice(shop_ids)}
        for cid in random.sample(claim_ids, min(1500, len(claim_ids)))
    ],

    "BILL_FOR_CLAIM": [
        {"bill_id": b["bill_id"], "claim_id": b["claim_id"]}
        for b in medical_bills
    ],

    "BILL_SUBMITTED_BY": [
        {"bill_id": b["bill_id"], "npi": b["npi"]}
        for b in medical_bills
    ],

    "PERSON_HAS_ADDRESS": [
        {"person_id": pid, "address_id": random.choice(address_ids)}
        for pid in person_ids
    ],

    "PERSON_HAS_PHONE": [
        {"person_id": pid, "phone_hash": random.choice(phone_hashes)}
        for pid in person_ids
    ],

    "PERSON_HAS_BANK": [
        {"person_id": pid, "account_id": random.choice(account_ids)}
        for pid in random.sample(person_ids, min(3000, len(person_ids)))
    ],

    "PERSON_EMPLOYED_BY": [
        {"person_id": pid, "employer_id": random.choice(employer_ids)}
        for pid in random.sample(person_ids, min(5000, len(person_ids)))
    ],

    "PERSON_HAS_DEPENDENT": [
        {"person_id": d["person_id"], "dependent_id": d["dependent_id"]}
        for d in dependents
    ],

    "PERSON_IS_EMPLOYEE": [
        {"person_id": e["person_id"], "employee_id": e["employee_id"]}
        for e in employees
    ],

    "PERSON_IN_FRAUD_RING": [
        {
            "person_id":   random.choice(person_ids),
            "ring_id":     random.choice(ring_ids),
            "role":        random.choice(["LEADER", "RECRUITER", "CLAIMANT", "PROVIDER", "RUNNER"]),
            "joined_date": random.choice(claims)["loss_date"],
        }
        for _ in range(800)
    ],

    "ADJUSTER_WORKS_FOR": [
        {"adjuster_id": a["adjuster_id"], "employer_id": random.choice(employer_ids)}
        for a in adjusters
    ],

    "ADJUSTER_REFERRED_SHOP": [
        {"adjuster_id": random.choice(adj_ids), "shop_id": sid, "count": random.randint(1, 50)}
        for sid in shop_ids
    ],

    "ADJUSTER_REFERRED_PROVIDER": [
        {"adjuster_id": random.choice(adj_ids), "npi": npi, "count": random.randint(1, 80)}
        for npi in npi_list
    ],

    "ATTORNEY_HAS_ADDRESS": [
        {"bar_id": a["bar_id"], "address_id": random.choice(address_ids)}
        for a in attorneys
    ],

    "PROVIDER_HAS_ADDRESS": [
        {"npi": p["npi"], "address_id": random.choice(address_ids)}
        for p in medical_providers
    ],

    "VEHICLE_IN_FLEET": [
        {"vin": vin, "fleet_id": random.choice(fleet_ids)}
        for vin in random.sample(vins, min(500, len(vins)))
    ],

    "POLICY_HAS_COVERAGE": [
        {"policy_id": c["policy_id"], "coverage_id": c["coverage_id"]}
        for c in coverage_lines
    ],

    "CLAIM_IN_RING": [
        {
            "claim_id": random.choice(claim_ids),
            "ring_id":  random.choice(ring_ids),
            "pattern":  random.choice(["MEDICAL_MILL", "STAGED_ACCIDENT", "PHANTOM_PASSENGER"]),
            "score":    round(random.uniform(0.6, 1.0), 3),
        }
        for _ in range(600)
    ],

    "SHARED_PHONE": [
        {
            "person_id_1": random.choice(person_ids),
            "person_id_2": random.choice(person_ids),
            "phone_hash":  random.choice(phone_hashes),
        }
        for _ in range(400)
    ],

    "SHARED_ADDRESS": [
        {
            "person_id_1": random.choice(person_ids),
            "person_id_2": random.choice(person_ids),
            "address_id":  random.choice(address_ids),
        }
        for _ in range(400)
    ],

    "CROSS_SYSTEM_LINKS": [
        {"person_id": x["person_id"], "xref_id": x["xref_id"]}
        for x in cross_system_ids
    ],

    "ISO_MATCH": [
        {
            "claim_id_1":  random.choice(claim_ids),
            "claim_id_2":  random.choice(claim_ids),
            "match_type":  random.choice(["EXACT", "FUZZY", "PARTIAL"]),
            "confidence":  round(random.uniform(0.7, 1.0), 3),
        }
        for _ in range(300)
    ],
}

# -----------------------------------------------------------------------------
# LOAD INTO NEO4J
# -----------------------------------------------------------------------------
print("\n=== CONNECTING TO NEO4J ===")
driver = get_driver()

load_nodes(driver, node_data)
load_relationships(driver, rel_data)
verify(driver)

driver.close()
print("\n=== PHASE B COMPLETE ===")
