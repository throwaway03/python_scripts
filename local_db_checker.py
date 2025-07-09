def local_db_check(internal_tx, blockchain_tx):
    
    internal_set = set(internal_tx)
    external_set = set(blockchain_tx)
    missing_txs = list(external_set.difference(internal_set))

    return missing_txs

db_transactions = [
    "0xabc111...", 
    "0xdef222...", 
    "0xghi333..."
]

extrenal_transactions = [
    "0xabc111...", 
    "0xdef222...", 
    "0xghi333...",
    "0xjkl444..." # This one is missing from our DB
]


missing = local_db_check(db_transactions, extrenal_transactions)
print(f"Missing transactions: {missing}")