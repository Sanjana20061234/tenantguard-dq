import random

def inject_all(data):
    """
    Injects exactly the specified corruptions for the demo.
    """
    inject_bug_1(data["accounts"])
    inject_bug_2(data["transactions"])
    inject_bug_3(data["holdings"])
    inject_bug_4(data["fee_schedules"])

def inject_bug_1(accounts):
    """BUG-1: 1 row with organisation_id = NULL in accounts. Must be caught by null_check (ERROR)"""
    # Pick the first account and set its org_id to None/empty string
    accounts[0]["organisation_id"] = ""

def inject_bug_2(transactions):
    """BUG-2: 1 duplicated (organisation_id, transaction_id) row. Must be caught by unique_key (ERROR).
    Also causes row count to be +1 vs manifest (row_count_reconciliation, WARNING)."""
    if not transactions: return
    row_to_dup = transactions[0].copy()
    # Inject canary string here since it has a text column
    row_to_dup["description"] = "SECRET_PII_CANARY_123"
    transactions.append(row_to_dup)
    
def inject_bug_3(holdings):
    """BUG-3: 1 holdings row whose organisation_id is org_4471 but portfolio_id belongs to org_8812.
    Must be caught by cross_tenant_check (ERROR).
    """
    target_idx = None
    for i, h in enumerate(holdings):
        if h["organisation_id"] == "org_4471":
            target_idx = i
            break
            
    if target_idx is not None:
        holdings[target_idx]["portfolio_id"] = "PRT-8812-0001"

def inject_bug_4(fee_schedules):
    """BUG-4: 1 negative fee_rate_bps. Must be caught by range_check (WARNING)"""
    if fee_schedules:
        fee_schedules[0]["fee_rate_bps"] = -10
