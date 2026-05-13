# =============================================================================
# LOADER — UNWIND + MERGE batches into AuraDB
# =============================================================================
import os
import time
from neo4j import GraphDatabase
from typing import List, Dict, Any

NEO4J_URI      = os.getenv("NEO4J_URI")
NEO4J_USER     = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")

BATCH_SIZE = 500   # AuraDB sweet spot

# -----------------------------------------------------------------------------
# DRIVER
# -----------------------------------------------------------------------------
def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def run_batch(session, query: str, rows: List[Dict], label: str):
    total = len(rows)
    loaded = 0
    for i in range(0, total, BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        session.run(query, rows=batch)
        loaded += len(batch)
        print(f"  {label}: {loaded}/{total}")
    print(f"  ✓ {label} complete — {total} nodes")

# -----------------------------------------------------------------------------
# MERGE QUERIES — one per node label
# -----------------------------------------------------------------------------
MERGES = {

    "FraudRing": (
        """UNWIND $rows AS r
           MERGE (n:FraudRing {ring_id: r.ring_id})
           SET n += r""",
    ),

    "Person": (
        """UNWIND $rows AS r
           MERGE (n:Person {person_id: r.person_id})
           SET n += r""",
    ),

    "Employee": (
        """UNWIND $rows AS r
           MERGE (n:Employee {employee_id: r.employee_id})
           SET n += r""",
    ),

    "Dependent": (
        """UNWIND $rows AS r
           MERGE (n:Dependent {dependent_id: r.dependent_id})
           SET n += r""",
    ),

    "Employer": (
        """UNWIND $rows AS r
           MERGE (n:Employer {employer_id: r.employer_id})
           SET n += r""",
    ),

    "Policy": (
        """UNWIND $rows AS r
           MERGE (n:Policy {policy_id: r.policy_id})
           SET n += r""",
    ),

    "CoverageLine": (
        """UNWIND $rows AS r
           MERGE (n:CoverageLine {coverage_id: r.coverage_id})
           SET n += r""",
    ),

    "Claim": (
        """UNWIND $rows AS r
           MERGE (n:Claim {claim_id: r.claim_id})
           SET n += r""",
    ),

    "ClaimVersion": (
        """UNWIND $rows AS r
           MERGE (n:ClaimVersion {version_id: r.version_id})
           SET n += r""",
    ),

    "ClaimPayment": (
        """UNWIND $rows AS r
           MERGE (n:ClaimPayment {payment_id: r.payment_id})
           SET n += r""",
    ),

    "MedicalProvider": (
        """UNWIND $rows AS r
           MERGE (n:MedicalProvider {npi: r.npi})
           SET n += r""",
    ),

    "MedicalBill": (
        """UNWIND $rows AS r
           MERGE (n:MedicalBill {bill_id: r.bill_id})
           SET n += r""",
    ),

    "RepairShop": (
        """UNWIND $rows AS r
           MERGE (n:RepairShop {shop_id: r.shop_id})
           SET n += r""",
    ),

    "Attorney": (
        """UNWIND $rows AS r
           MERGE (n:Attorney {bar_id: r.bar_id})
           SET n += r""",
    ),

    "TowCompany": (
        """UNWIND $rows AS r
           MERGE (n:TowCompany {company_id: r.company_id})
           SET n += r""",
    ),

    "Adjuster": (
        """UNWIND $rows AS r
           MERGE (n:Adjuster {adjuster_id: r.adjuster_id})
           SET n += r""",
    ),

    "Vehicle": (
        """UNWIND $rows AS r
           MERGE (n:Vehicle {vin: r.vin})
           SET n += r""",
    ),

    "Fleet": (
        """UNWIND $rows AS r
           MERGE (n:Fleet {fleet_id: r.fleet_id})
           SET n += r""",
    ),

    "Address": (
        """UNWIND $rows AS r
           MERGE (n:Address {address_id: r.address_id})
           SET n += r""",
    ),

    "Phone": (
        """UNWIND $rows AS r
           MERGE (n:Phone {phone_hash: r.phone_hash})
           SET n += r""",
    ),

    "BankAccount": (
        """UNWIND $rows AS r
           MERGE (n:BankAccount {account_id: r.account_id})
           SET n += r""",
    ),

    "CrossSystemID": (
        """UNWIND $rows AS r
           MERGE (n:CrossSystemID {xref_id: r.xref_id})
           SET n += r""",
    ),

    "LitigationEvent": (
        """UNWIND $rows AS r
           MERGE (n:LitigationEvent {litigation_id: r.litigation_id})
           SET n += r""",
    ),

    "InjuryRecord": (
        """UNWIND $rows AS r
           MERGE (n:InjuryRecord {injury_id: r.injury_id})
           SET n += r""",
    ),
}

# -----------------------------------------------------------------------------
# RELATIONSHIP MERGES (32 relationships)
# -----------------------------------------------------------------------------
REL_MERGES = {

    "CLAIM_UNDER_POLICY": """
        UNWIND $rows AS r
        MATCH (c:Claim {claim_id: r.claim_id})
        MATCH (p:Policy {policy_id: r.policy_id})
        MERGE (c)-[:UNDER_POLICY]->(p)""",

    "CLAIM_HAS_VERSION": """
        UNWIND $rows AS r
        MATCH (c:Claim {claim_id: r.claim_id})
        MATCH (v:ClaimVersion {version_id: r.version_id})
        MERGE (c)-[:HAS_VERSION]->(v)""",

    "CLAIM_HAS_PAYMENT": """
        UNWIND $rows AS r
        MATCH (c:Claim {claim_id: r.claim_id})
        MATCH (p:ClaimPayment {payment_id: r.payment_id})
        MERGE (c)-[:HAS_PAYMENT]->(p)""",

    "CLAIM_HAS_INJURY": """
        UNWIND $rows AS r
        MATCH (c:Claim {claim_id: r.claim_id})
        MATCH (i:InjuryRecord {injury_id: r.injury_id})
        MERGE (c)-[:HAS_INJURY]->(i)""",

    "CLAIM_HAS_LITIGATION": """
        UNWIND $rows AS r
        MATCH (c:Claim {claim_id: r.claim_id})
        MATCH (l:LitigationEvent {litigation_id: r.litigation_id})
        MERGE (c)-[:HAS_LITIGATION]->(l)""",

    "CLAIM_FILED_BY": """
        UNWIND $rows AS r
        MATCH (c:Claim {claim_id: r.claim_id})
        MATCH (p:Person {person_id: r.person_id})
        MERGE (c)-[:FILED_BY]->(p)""",

    "CLAIM_HANDLED_BY": """
        UNWIND $rows AS r
        MATCH (c:Claim {claim_id: r.claim_id})
        MATCH (a:Adjuster {adjuster_id: r.adjuster_id})
        MERGE (c)-[:HANDLED_BY]->(a)""",

    "CLAIM_INVOLVES_VEHICLE": """
        UNWIND $rows AS r
        MATCH (c:Claim {claim_id: r.claim_id})
        MATCH (v:Vehicle {vin: r.vin})
        MERGE (c)-[:INVOLVES_VEHICLE]->(v)""",

    "CLAIM_INVOLVES_PROVIDER": """
        UNWIND $rows AS r
        MATCH (c:Claim {claim_id: r.claim_id})
        MATCH (p:MedicalProvider {npi: r.npi})
        MERGE (c)-[:INVOLVES_PROVIDER]->(p)""",

    "CLAIM_REPRESENTED_BY": """
        UNWIND $rows AS r
        MATCH (c:Claim {claim_id: r.claim_id})
        MATCH (a:Attorney {bar_id: r.bar_id})
        MERGE (c)-[:REPRESENTED_BY]->(a)""",

    "CLAIM_REPAIRED_BY": """
        UNWIND $rows AS r
        MATCH (c:Claim {claim_id: r.claim_id})
        MATCH (s:RepairShop {shop_id: r.shop_id})
        MERGE (c)-[:REPAIRED_BY]->(s)""",

    "BILL_FOR_CLAIM": """
        UNWIND $rows AS r
        MATCH (b:MedicalBill {bill_id: r.bill_id})
        MATCH (c:Claim {claim_id: r.claim_id})
        MERGE (b)-[:BILL_FOR]->(c)""",

    "BILL_SUBMITTED_BY": """
        UNWIND $rows AS r
        MATCH (b:MedicalBill {bill_id: r.bill_id})
        MATCH (p:MedicalProvider {npi: r.npi})
        MERGE (b)-[:SUBMITTED_BY]->(p)""",

    "PERSON_HAS_ADDRESS": """
        UNWIND $rows AS r
        MATCH (p:Person {person_id: r.person_id})
        MATCH (a:Address {address_id: r.address_id})
        MERGE (p)-[:HAS_ADDRESS]->(a)""",

    "PERSON_HAS_PHONE": """
        UNWIND $rows AS r
        MATCH (p:Person {person_id: r.person_id})
        MATCH (ph:Phone {phone_hash: r.phone_hash})
        MERGE (p)-[:HAS_PHONE]->(ph)""",

    "PERSON_HAS_BANK": """
        UNWIND $rows AS r
        MATCH (p:Person {person_id: r.person_id})
        MATCH (b:BankAccount {account_id: r.account_id})
        MERGE (p)-[:HAS_BANK_ACCOUNT]->(b)""",

    "PERSON_EMPLOYED_BY": """
        UNWIND $rows AS r
        MATCH (p:Person {person_id: r.person_id})
        MATCH (e:Employer {employer_id: r.employer_id})
        MERGE (p)-[:EMPLOYED_BY]->(e)""",

    "PERSON_HAS_DEPENDENT": """
        UNWIND $rows AS r
        MATCH (p:Person {person_id: r.person_id})
        MATCH (d:Dependent {dependent_id: r.dependent_id})
        MERGE (p)-[:HAS_DEPENDENT]->(d)""",

    "PERSON_IS_EMPLOYEE": """
        UNWIND $rows AS r
        MATCH (p:Person {person_id: r.person_id})
        MATCH (e:Employee {employee_id: r.employee_id})
        MERGE (p)-[:IS_EMPLOYEE]->(e)""",

    "PERSON_IN_FRAUD_RING": """
        UNWIND $rows AS r
        MATCH (p:Person {person_id: r.person_id})
        MATCH (fr:FraudRing {ring_id: r.ring_id})
        MERGE (p)-[:MEMBER_OF {role: r.role, joined_date: r.joined_date}]->(fr)""",

    "ADJUSTER_WORKS_FOR": """
        UNWIND $rows AS r
        MATCH (a:Adjuster {adjuster_id: r.adjuster_id})
        MATCH (e:Employer {employer_id: r.employer_id})
        MERGE (a)-[:WORKS_FOR]->(e)""",

    "ADJUSTER_REFERRED_SHOP": """
        UNWIND $rows AS r
        MATCH (a:Adjuster {adjuster_id: r.adjuster_id})
        MATCH (s:RepairShop {shop_id: r.shop_id})
        MERGE (a)-[:REFERRED {count: r.count}]->(s)""",

    "ADJUSTER_REFERRED_PROVIDER": """
        UNWIND $rows AS r
        MATCH (a:Adjuster {adjuster_id: r.adjuster_id})
        MATCH (p:MedicalProvider {npi: r.npi})
        MERGE (a)-[:REFERRED {count: r.count}]->(p)""",

    "ATTORNEY_HAS_ADDRESS": """
        UNWIND $rows AS r
        MATCH (a:Attorney {bar_id: r.bar_id})
        MATCH (addr:Address {address_id: r.address_id})
        MERGE (a)-[:HAS_ADDRESS]->(addr)""",

    "PROVIDER_HAS_ADDRESS": """
        UNWIND $rows AS r
        MATCH (p:MedicalProvider {npi: r.npi})
        MATCH (a:Address {address_id: r.address_id})
        MERGE (p)-[:HAS_ADDRESS]->(a)""",

    "VEHICLE_IN_FLEET": """
        UNWIND $rows AS r
        MATCH (v:Vehicle {vin: r.vin})
        MATCH (f:Fleet {fleet_id: r.fleet_id})
        MERGE (v)-[:IN_FLEET]->(f)""",

    "POLICY_HAS_COVERAGE": """
        UNWIND $rows AS r
        MATCH (p:Policy {policy_id: r.policy_id})
        MATCH (c:CoverageLine {coverage_id: r.coverage_id})
        MERGE (p)-[:HAS_COVERAGE]->(c)""",

    "CLAIM_IN_RING": """
        UNWIND $rows AS r
        MATCH (c:Claim {claim_id: r.claim_id})
        MATCH (fr:FraudRing {ring_id: r.ring_id})
        MERGE (c)-[:LINKED_TO_RING {pattern: r.pattern, score: r.score}]->(fr)""",

    "SHARED_PHONE": """
        UNWIND $rows AS r
        MATCH (p1:Person {person_id: r.person_id_1})
        MATCH (p2:Person {person_id: r.person_id_2})
        MATCH (ph:Phone {phone_hash: r.phone_hash})
        MERGE (p1)-[:SHARES_PHONE {phone_hash: r.phone_hash}]->(p2)""",

    "SHARED_ADDRESS": """
        UNWIND $rows AS r
        MATCH (p1:Person {person_id: r.person_id_1})
        MATCH (p2:Person {person_id: r.person_id_2})
        MERGE (p1)-[:SHARES_ADDRESS {address_id: r.address_id}]->(p2)""",

    "CROSS_SYSTEM_LINKS": """
        UNWIND $rows AS r
        MATCH (p:Person {person_id: r.person_id})
        MATCH (x:CrossSystemID {xref_id: r.xref_id})
        MERGE (p)-[:HAS_XREF]->(x)""",

    "ISO_MATCH": """
        UNWIND $rows AS r
        MATCH (c1:Claim {claim_id: r.claim_id_1})
        MATCH (c2:Claim {claim_id: r.claim_id_2})
        MERGE (c1)-[:ISO_MATCH {match_type: r.match_type, confidence: r.confidence}]->(c2)""",
}

# -----------------------------------------------------------------------------
# LOAD ALL NODES
# -----------------------------------------------------------------------------
def load_nodes(driver, data: Dict[str, List]):
    with driver.session(database=NEO4J_DATABASE) as session:
        for label, rows in data.items():
            if not rows:
                continue
            query = MERGES[label][0]
            print(f"\nLoading {label}...")
            run_batch(session, query, rows, label)

# -----------------------------------------------------------------------------
# LOAD ALL RELATIONSHIPS
# -----------------------------------------------------------------------------
def load_relationships(driver, rel_data: Dict[str, List]):
    with driver.session(database=NEO4J_DATABASE) as session:
        for rel_name, rows in rel_data.items():
            if not rows:
                continue
            query = REL_MERGES[rel_name]
            print(f"\nLoading relationship {rel_name}...")
            run_batch(session, query, rows, rel_name)

# -----------------------------------------------------------------------------
# VERIFY
# -----------------------------------------------------------------------------
def verify(driver):
    print("\n=== VERIFICATION ===")
    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run("""
            CALL apoc.meta.stats()
            YIELD labels, nodeCount, relCount
            RETURN labels, nodeCount, relCount
        """)
        record = result.single()
        if record:
            print(f"Total nodes: {record['nodeCount']}")
            print(f"Total rels:  {record['relCount']}")
            for label, count in sorted(record["labels"].items()):
                print(f"  {label}: {count}")
