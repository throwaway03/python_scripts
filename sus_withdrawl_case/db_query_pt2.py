import csv
import sqlite3

INPUT_CSV = "sus_w.csv"
DB_FILE = "investigation.db"

def extract_more_data(db_path, csv_path):

    new_records = []
    conn = None

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        with open(csv_path, 'r', newline='') as f:
            reader = csv.DictReader(f)

            for row in reader:
                user_id = row['user_id']

                sql_query = "SELECT kyc_level, created_at, country_code FROM users WHERE user_id = ?"
                cursor.execute(sql_query, (user_id,)) #comma makes it a tuple
                user_details = cursor.fetchone()

                if user_details: 
                    record = {
                        'withdrawal_id': int(row['withdrawal_id']),
                        'user_id': int(user_id),
                        'amount': float(row['amount']),
                        'tx_hash': row['tx_hash'],
                        'withdrawal_created_at': row['created_at'],
                        'user_kyc_level': user_details[0],
                        'user_created_at': user_details[1],
                        'user_country_code': user_details[2]
                    }
                    new_records.append(record)
                else: print(f"No details for {user_id}. Skip.")

        return new_records
    
    except sqlite3.Error as e:
        print(f"Error @ {e}")
        return None
    
    except (IOError, csv.Error) as e:
        print(f"Another error @ {e}")
        return None

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    enriched_data = extract_more_data(DB_FILE, INPUT_CSV)

    if enriched_data is not None:
        print(f"\nSuccessfully added {len(enriched_data)} records.")
        
        if enriched_data:
            print("\nSample of the new first record.")
            first_record = enriched_data[0]
            for key, value in first_record.items():
                print(f"  {key}: {value}")
    else:
        print("\nFailed.")