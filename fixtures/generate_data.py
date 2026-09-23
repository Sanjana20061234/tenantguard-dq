import csv
import json
import random
import argparse
from pathlib import Path

# Seed for deterministic generation
random.seed(42)

ORGS = ["org_8812", "org_4471", "org_9020"]

# We will generate dictionaries for each table
data = {
    "organisations": [],
    "advisors": [],
    "clients": [],
    "accounts": [],
    "portfolios": [],
    "securities": [],
    "holdings": [],
    "trades": [],
    "transactions": [],
    "fee_schedules": [],
    "statements": []
}

def generate_clean_data():
    # 1. Organisations
    for org in ORGS:
        data["organisations"].append({"organisation_id": org, "name": f"{org} Wealth Management"})
    
    # 2. Advisors (~6 per org)
    advisors_by_org = {org: [] for org in ORGS}
    for org in ORGS:
        for i in range(1, 7):
            adv_id = f"ADV-{org[-4:]}-{i:03d}"
            advisors_by_org[org].append(adv_id)
            data["advisors"].append({
                "organisation_id": org,
                "advisor_id": adv_id,
                "name": f"Advisor {i} of {org}"
            })
            
    # 3. Clients (~25 per org)
    clients_by_org = {org: [] for org in ORGS}
    for org in ORGS:
        for i in range(1, 26):
            client_id = f"CLI-{org[-4:]}-{i:04d}"
            clients_by_org[org].append(client_id)
            data["clients"].append({
                "organisation_id": org,
                "client_id": client_id,
                "advisor_id": random.choice(advisors_by_org[org]),
                "name": f"Client {i} of {org}"
            })
            
    # 4. Accounts (~40 per org)
    accounts_by_org = {org: [] for org in ORGS}
    for org in ORGS:
        for i in range(1, 41):
            acc_id = f"ACC-{org[-4:]}-{i:04d}"
            accounts_by_org[org].append(acc_id)
            data["accounts"].append({
                "organisation_id": org,
                "account_id": acc_id,
                "client_id": random.choice(clients_by_org[org]),
                "type": random.choice(["Individual", "Joint", "Trust"])
            })

    # 5. Portfolios (~60 per org)
    portfolios_by_org = {org: [] for org in ORGS}
    for org in ORGS:
        for i in range(1, 61):
            port_id = f"PRT-{org[-4:]}-{i:04d}"
            portfolios_by_org[org].append(port_id)
            data["portfolios"].append({
                "organisation_id": org,
                "portfolio_id": port_id,
                "account_id": random.choice(accounts_by_org[org]),
                "strategy": random.choice(["Growth", "Income", "Balanced"])
            })

    # 6. Securities (~40 per org)
    securities_by_org = {org: [] for org in ORGS}
    for org in ORGS:
        for i in range(1, 41):
            sec_id = f"SEC-{org[-4:]}-{i:04d}"
            securities_by_org[org].append(sec_id)
            data["securities"].append({
                "organisation_id": org,
                "security_id": sec_id,
                "symbol": f"SYM{i}",
                "asset_class": random.choice(["Equity", "Fixed Income", "Cash"])
            })
            
    # 7. Holdings (~300 per org)
    for org in ORGS:
        for i in range(1, 301):
            hold_id = f"HLD-{org[-4:]}-{i:05d}"
            data["holdings"].append({
                "organisation_id": org,
                "holding_id": hold_id,
                "portfolio_id": random.choice(portfolios_by_org[org]),
                "security_id": random.choice(securities_by_org[org]),
                "quantity": round(random.uniform(10, 1000), 2)
            })

    # 8. Trades (~500 per org)
    for org in ORGS:
        for i in range(1, 501):
            trade_id = f"TRD-{org[-4:]}-{i:05d}"
            data["trades"].append({
                "organisation_id": org,
                "trade_id": trade_id,
                "portfolio_id": random.choice(portfolios_by_org[org]),
                "security_id": random.choice(securities_by_org[org]),
                "trade_date": "2023-10-01",
                "quantity": round(random.uniform(1, 100), 2),
                "price": round(random.uniform(10, 500), 2)
            })

    # 9. Transactions (~2000 per org)
    for org in ORGS:
        for i in range(1, 2001):
            txn_id = f"TXN-{org[-4:]}-{i:05d}"
            data["transactions"].append({
                "organisation_id": org,
                "transaction_id": txn_id,
                "account_id": random.choice(accounts_by_org[org]),
                "amount": round(random.uniform(-5000, 5000), 2),
                "description": "Standard Transaction"
            })

    # 10. Fee Schedules (1 per account)
    for org in ORGS:
        for acc_id in accounts_by_org[org]:
            data["fee_schedules"].append({
                "organisation_id": org,
                "fee_schedule_id": f"FEE-{acc_id}",
                "account_id": acc_id,
                "fee_rate_bps": random.choice([25, 50, 75, 100])
            })

    # 11. Statements (2 per account)
    for org in ORGS:
        for acc_id in accounts_by_org[org]:
            for m in [1, 2]:
                data["statements"].append({
                    "organisation_id": org,
                    "statement_id": f"STMT-{acc_id}-M{m}",
                    "account_id": acc_id,
                    "statement_date": f"2023-0{m}-01",
                    "balance": round(random.uniform(10000, 1000000), 2)
                })

def write_data(out_dir: Path, manifest: dict):
    out_dir.mkdir(parents=True, exist_ok=True)
    for table, rows in data.items():
        manifest[table] = len(rows)
        with open(out_dir / f"{table}.csv", "w", newline="") as f:
            if not rows:
                continue
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["clean", "corrupt"], required=True)
    args = parser.parse_args()

    # Generate clean data first
    generate_clean_data()
    
    # Store manifest BEFORE corruptions (because row count reconciliation is expected vs clean manifest)
    manifest = {}
    for t in data:
        manifest[t] = len(data[t])
        
    out_dir = Path(f"fixtures/data/{args.mode}")
    
    if args.mode == "corrupt":
        import corruptions
        corruptions.inject_all(data)
        
    # Write out data
    write_data(out_dir, manifest)
    
    if args.mode == "clean":
        # Write manifest only in clean mode
        with open("fixtures/manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    main()
