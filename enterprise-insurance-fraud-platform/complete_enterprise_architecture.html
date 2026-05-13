
<style>
.wrap { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 16px; }
.sec { margin-bottom: 20px; }
.sec-title { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: var(--color-text-tertiary); margin-bottom: 10px; padding-bottom: 6px; border-bottom: 0.5px solid var(--color-border-tertiary); }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.grid3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
.card { background: var(--color-background-secondary); border: 0.5px solid var(--color-border-tertiary); border-radius: 8px; padding: 12px 14px; }
.card-title { font-size: 13px; font-weight: 700; color: var(--color-text-primary); margin-bottom: 6px; }
.card-body { font-size: 12px; color: var(--color-text-secondary); line-height: 1.7; }
.badge { display: inline-block; font-size: 9px; font-weight: 700; padding: 1px 6px; border-radius: 8px; margin: 1px; }
.b-red    { background: var(--color-background-danger);  color: var(--color-text-danger);  }
.b-green  { background: var(--color-background-success); color: var(--color-text-success); }
.b-blue   { background: var(--color-background-info);    color: var(--color-text-info);    }
.b-yellow { background: var(--color-background-warning); color: var(--color-text-warning); }
.b-gray   { background: var(--color-background-tertiary); color: var(--color-text-tertiary); }
.b-purple { background: rgba(128,90,213,.2); color: #b794f4; }
.layer { border-radius: 8px; padding: 12px 14px; margin-bottom: 8px; border: 0.5px solid var(--color-border-tertiary); }
.layer-num { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; margin-bottom: 4px; }
.layer-title { font-size: 14px; font-weight: 700; color: var(--color-text-primary); margin-bottom: 6px; }
.layer-body { font-size: 12px; color: var(--color-text-secondary); line-height: 1.7; }
.l1 { background: rgba(229,62,62,.06);   border-color: rgba(229,62,62,.2);   }
.l2 { background: rgba(214,158,46,.06);  border-color: rgba(214,158,46,.2);  }
.l3 { background: rgba(56,161,105,.06);  border-color: rgba(56,161,105,.2);  }
.l4 { background: rgba(99,102,241,.06);  border-color: rgba(99,102,241,.2);  }
.l5 { background: rgba(9,135,160,.06);   border-color: rgba(9,135,160,.2);   }
.l6 { background: rgba(128,90,213,.06);  border-color: rgba(128,90,213,.2);  }
.l7 { background: rgba(183,121,31,.06);  border-color: rgba(183,121,31,.2);  }
.l8 { background: rgba(113,128,150,.06); border-color: rgba(113,128,150,.2); }
.phase-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.phase-table th { text-align: left; font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; color: var(--color-text-tertiary); padding: 6px 8px; border-bottom: 0.5px solid var(--color-border-tertiary); }
.phase-table td { padding: 8px 8px; border-bottom: 0.5px solid var(--color-border-tertiary); color: var(--color-text-secondary); vertical-align: top; font-size: 12px; line-height: 1.5; }
.phase-table td:first-child { font-weight: 600; color: var(--color-text-primary); white-space: nowrap; }
.phase-table tr:last-child td { border-bottom: none; }
</style>

<div class="wrap">

<!-- ARCHITECTURE LAYERS -->
<div class="sec">
<div class="sec-title">8-Layer Enterprise Architecture</div>

<div class="layer l1">
  <div class="layer-num" style="color:#fc8181">Layer 1 — Data Sources (12 systems)</div>
  <div class="layer-body">
    <span class="badge b-blue">Internal</span> Guidewire Claims · Duck Creek Policy · TriZetto Medical Billing · SAP Finance · Salesforce CRM · Workday HR/Benefits · Sedgwick WC TPA<br>
    <span class="badge b-yellow">External</span> ISO ClaimSearch · LexisNexis Risk · NICB · CMS Provider Exclusions · NOAA Weather · DMV Feeds · OFAC Sanctions · Court Records · IRS TIN
  </div>
</div>

<div class="layer l2">
  <div class="layer-num" style="color:#f6ad55">Layer 2 — Ingestion Pipeline (Simulated Kafka)</div>
  <div class="layer-body">
    <span class="badge b-yellow">Topics</span> claims.fnol · claims.update · policy.change · medical.bill · repair.invoice · payment.issued · iso.claimsearch · external.enrichment<br>
    <span class="badge b-gray">Pattern</span> Batch (nightly 100K) + Real-time (&lt;500ms per claim) · Same MERGE logic · Swap real Kafka in Phase 6
  </div>
</div>

<div class="layer l3">
  <div class="layer-num" style="color:#68d391">Layer 3 — Multi-Modal AI Processing</div>
  <div class="layer-body">
    <span class="badge b-green">CV Pipeline</span> Damage photos · Repair invoices · Accident scenes · Medical docs<br>
    <span class="badge b-green">5 CV Layers</span> EXIF/Metadata · ELA+FFT Pixel Forensics · Duplicate Detection · Cross-Document Consistency · Temporal Consistency<br>
    <span class="badge b-green">OCR+LLM</span> Entity extraction → graph loading · Anomaly flagging · Template similarity detection<br>
    <span class="badge b-green">Synthetic ID</span> Discriminative detection first → generative detection capability designed in
  </div>
</div>

<div class="layer l4">
  <div class="layer-num" style="color:#a5b4fc">Layer 4 — Entity Resolution</div>
  <div class="layer-body">
    <span class="badge b-blue">Cross-system</span> Master person_id across Guidewire + Salesforce + Workday + Sedgwick<br>
    <span class="badge b-blue">Fuzzy match</span> Names · Phones · Addresses · DOB · SSN-last4 · Device fingerprint<br>
    <span class="badge b-blue">ISO match</span> Cross-carrier identity resolution via ISO ClaimSearch xref
  </div>
</div>

<div class="layer l5">
  <div class="layer-num" style="color:#76e4f7">Layer 5 — Graph Store (Neo4j AuraDB)</div>
  <div class="layer-body">
    <span class="badge b-blue">24 node labels</span> Claim · ClaimVersion · CoverageLine · ClaimPayment · Person · Employee · Dependent · Policy · Vehicle · Fleet · MedicalProvider · MedicalBill · RepairShop · Attorney · TowCompany · Employer · Address · Phone · CrossSystemID · Adjuster · BankAccount · LitigationEvent · InjuryRecord · FraudRing<br>
    <span class="badge b-blue">Temporal</span> Properties + timestamps on all nodes · GDS temporal algorithms · Time-series graph for complex patterns (Phase 2)
  </div>
</div>

<div class="layer l6">
  <div class="layer-num" style="color:#d6bcfa">Layer 6 — Intelligence Engine</div>
  <div class="layer-body">
    <span class="badge b-purple">GDS</span> Connected Components · Louvain Community · PageRank · Betweenness Centrality · Temporal WCC<br>
    <span class="badge b-purple">GNN</span> PyTorch Geometric designed in · Optional activation · Heterogeneous graph neural network for collusion<br>
    <span class="badge b-purple">Scoring</span> 21 fraud patterns · LOB-specific weights · Payment hold logic · Cross-carrier signals from ISO
  </div>
</div>

<div class="layer l7">
  <div class="layer-num" style="color:#fbd38d">Layer 7 — Agentic AI (Human-in-the-Loop)</div>
  <div class="layer-body">
    <span class="badge b-yellow">Co-pilot</span> AI assembles evidence package · Suggests investigation steps · Drafts SIU referral narrative<br>
    <span class="badge b-yellow">Human</span> Analyst reviews · Approves/rejects referral · Adds external evidence · Closes case<br>
    <span class="badge b-yellow">Autonomous</span> Low-risk only: duplicate detection · OFAC screening · Payment hold triggers
  </div>
</div>

<div class="layer l8">
  <div class="layer-num" style="color:#a0aec0">Layer 8 — Investigator Dashboard</div>
  <div class="layer-body">
    <span class="badge b-gray">Views</span> Graph ring visualization · Temporal timeline · Geospatial map · Adjuster workqueue · Cross-carrier hits<br>
    <span class="badge b-gray">Actions</span> SIU referral · Payment hold · Watchlist flag · Case notes · Evidence upload
  </div>
</div>
</div>

<!-- FRAUD PATTERNS -->
<div class="sec">
<div class="sec-title">21 Fraud Patterns across 6 Categories</div>
<div class="grid2">

<div class="card">
  <div class="card-title" style="color:#fc8181">Cat 1 — Healthcare/Medical</div>
  <div class="card-body">
    <span class="badge b-red">HIGH</span> Medical mill (1 doctor → 50+ claims)<br>
    <span class="badge b-red">HIGH</span> CPT upcoding (billed vs allowed ratio)<br>
    <span class="badge b-red">HIGH</span> Phantom treatment (no facility record)<br>
    <span class="badge b-yellow">MED</span> Duplicate billing across carriers<br>
    <span class="badge b-yellow">MED</span> Unbundling CPT codes<br>
    <span class="badge b-green">LOW</span> Exaggerated soft tissue injury
  </div>
</div>

<div class="card">
  <div class="card-title" style="color:#f6ad55">Cat 2 — Property-Specific</div>
  <div class="card-body">
    <span class="badge b-red">HIGH</span> Arson ring (multi-property, same owner/agent)<br>
    <span class="badge b-red">HIGH</span> Flood fraud (pre-existing damage claimed)<br>
    <span class="badge b-yellow">MED</span> Contractor collusion (inflated estimates)<br>
    <span class="badge b-yellow">MED</span> Contents inflation (no purchase records)<br>
    <span class="badge b-green">LOW</span> Post-loss policy inception
  </div>
</div>

<div class="card">
  <div class="card-title" style="color:#76e4f7">Cat 3 — Temporal/Sequence</div>
  <div class="card-body">
    <span class="badge b-red">HIGH</span> Claim velocity (3+ claims in 90 days)<br>
    <span class="badge b-red">HIGH</span> Impossible timeline (treatment before incident)<br>
    <span class="badge b-yellow">MED</span> Reserve pattern anomaly (rapid escalation)<br>
    <span class="badge b-yellow">MED</span> Policy lapse/reinstate cycle before claim<br>
    <span class="badge b-green">LOW</span> Seasonal fraud clustering
  </div>
</div>

<div class="card">
  <div class="card-title" style="color:#a5b4fc">Cat 4 — Identity & Synthetic</div>
  <div class="card-body">
    <span class="badge b-red">HIGH</span> Synthetic identity (thin credit file + new SSN)<br>
    <span class="badge b-red">HIGH</span> Identity takeover (address/phone sudden change)<br>
    <span class="badge b-yellow">MED</span> Phantom passenger recycling<br>
    <span class="badge b-green">LOW</span> Address fraud (rate territory mismatch)
  </div>
</div>

<div class="card">
  <div class="card-title" style="color:#fbd38d">Cat 5 — Insider/Adjuster</div>
  <div class="card-body">
    <span class="badge b-red">HIGH</span> Adjuster + shop collusion (approval rate anomaly)<br>
    <span class="badge b-red">HIGH</span> Adjuster + attorney pipeline (settlement inflation)<br>
    <span class="badge b-yellow">MED</span> Phantom payment (payee = adjuster network)<br>
    <span class="badge b-yellow">MED</span> Reopened closed claims pattern
  </div>
</div>

<div class="card">
  <div class="card-title" style="color:#68d391">Cat 6 — Cross-Carrier (ISO)</div>
  <div class="card-body">
    <span class="badge b-red">HIGH</span> Same incident filed at 2+ carriers<br>
    <span class="badge b-red">HIGH</span> Serial claimant across carriers (ISO hit)<br>
    <span class="badge b-yellow">MED</span> Provider excluded at one carrier still billing another<br>
    <span class="badge b-yellow">MED</span> Cross-carrier medical mill network
  </div>
</div>

</div>
</div>

<!-- BUILD PHASES -->
<div class="sec">
<div class="sec-title">Build Phases — Production Roadmap</div>
<table class="phase-table">
<thead>
  <tr><th>Phase</th><th>Deliverable</th><th>Key Components</th><th>AuraDB Nodes</th></tr>
</thead>
<tbody>
<tr>
  <td>A — Schema</td>
  <td>Production Neo4j schema</td>
  <td>24 node labels · 32 relationships · all constraints · temporal indexes</td>
  <td>0 (schema only)</td>
</tr>
<tr>
  <td>B — Data Generator</td>
  <td>50K node production dataset</td>
  <td>5 source systems · 21 fraud patterns · 10 years · Hartford geography · ISO simulation</td>
  <td>~50K nodes</td>
</tr>
<tr>
  <td>C — Entity Resolution</td>
  <td>Cross-system ID pipeline</td>
  <td>Fuzzy match · master ID · CrossSystemID nodes · ISO xref</td>
  <td>+5K xref nodes</td>
</tr>
<tr>
  <td>D — Intelligence Engine</td>
  <td>GDS + scoring all 21 patterns</td>
  <td>Temporal GDS · LOB weights · payment hold · ISO signal · GNN design-in</td>
  <td>+score properties</td>
</tr>
<tr>
  <td>E — Multi-Modal AI</td>
  <td>CV + OCR + LLM pipeline</td>
  <td>5-layer CV · entity extraction · anomaly detection · synthetic ID discriminator</td>
  <td>+image metadata nodes</td>
</tr>
<tr>
  <td>F — Agentic Co-pilot</td>
  <td>Human-in-loop investigator</td>
  <td>Evidence assembly · SIU narrative · analyst approval workflow</td>
  <td>+case nodes</td>
</tr>
<tr>
  <td>G — Dashboard v2</td>
  <td>Production investigator UI</td>
  <td>Timeline · geo map · cross-carrier view · adjuster queue · evidence panel</td>
  <td>read only</td>
</tr>
<tr>
  <td>H — GNN (Optional)</td>
  <td>PyTorch Geometric collusion</td>
  <td>Heterogeneous GNN · trained on labeled rings · replaces/augments GDS Louvain</td>
  <td>read only</td>
</tr>
</tbody>
</table>
</div>

</div>
