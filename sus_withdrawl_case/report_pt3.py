import collections
from  datetime import datetime, timedelta

from db_query_pt2 import DB_FILE, INPUT_CSV, extract_more_data

RECENT_THRESHOLD_DAYS = 7

def analyze_and_report(records):

    if not records:
        print("No data to analyze")
        return None
    
    total_withdrawn_amount = 0
    unqiue_users_id = set()
    country_counter = collections.Counter()
    kyc_level_counter = collections.Counter()
    recent_account_count = 0
    now = datetime.now()

    for record in records:

        total_withdrawn_amount += record['amount']
        unqiue_users_id.add(record['user_id'])
        country_counter[record['user_country_code']] += 1
        kyc_level_counter[record['user_kyc_level']] += 1

        try:
            user_creation_date = datetime.strptime(record['user_created_at'], '%Y-%m-%d %H:%M:%S.%f')
            if now - user_creation_date < timedelta(days=RECENT_THRESHOLD_DAYS):
                recent_account_count += 1
        except (ValueError, TypeError):
            print(f"Couldn't parse {record['user_created_at']}")
        
    print("\n" + "="*50)
    print(" ANOMALOUS AETHERIUM (AETH) WITHDRAWAL REPORT")
    print("="*50)
    print("\n--- Overall Summary ---")
    print(f"Total Amount Withdrawn: {total_withdrawn_amount:,.2f} AETH")
    print(f"Total Number of Withdrawals: {len(records)}")
    print(f"Number of Unique Users Involved: {len(unqiue_users_id)}")
    print("\n--- User Profile Analysis ---") 
    print("\n1. Withdrawals by Country:")   

    # .most_common() returns a list of (item, count) tuples
    for country, count in country_counter.most_common():
        print(f"  - {country}: {count} withdrawal(s)")
    print("\n2. Withdrawals by KYC Level:")

    for level, count in kyc_level_counter.most_common():
        print(f"  - KYC Level {level}: {count} withdrawal(s)")
        
    print(f"\n3. Recently Created Accounts (last {RECENT_THRESHOLD_DAYS} days):")
    print(f"  - {recent_account_count} out of {len(records)} withdrawals came from recently created accounts.")

    print("\n" + "="*50)
    print(" END OF REPORT")
    print("="*50)

if __name__ == "__main__":
    print("Running Investigation Pipeline")
    
    enriched_data = extract_more_data(DB_FILE, INPUT_CSV)
    
    if enriched_data:
        analyze_and_report(enriched_data)
    else:
        print("\nPipeline failed at data enrichment step.")