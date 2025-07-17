import sqlite3
import csv

DB_FILE = "investigation.db"
OUTPUT_FILE = "sus_w.csv"

def extract_data(db_path, output_path):
    """
    Investigating recent(<24 hours) suspicous withdrawls of new low-liquidity crypto from the system 
    """

    query = """
    SELECT 
        wd.withdrawal_id, wd.user_id, wd.amount, wd.tx_hash, wd.created_at
    FROM 
        users u
    JOIN 
        withdrawals wd ON u.user_id=wd.user_id
    WHERE 
        wd.asset = 'AETH' 
        AND wd.status = 'success' 
        AND amount >= 1000 
        AND wd.created_at >= datetime('now', '-24 hours')
    """

    conn = None
    try: 
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(query)

        result = cursor.fetchall()

        if not result:
            print("Nothing found")
            return 0
    
        print(f"Found {len(result)} records. Writing to {output_path}")
        with open(output_path, "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            header = [description[0] for description in cursor.description]
            csv_writer.writerow(header)
            csv_writer.writerows(result)
    
        print(f"Success!")
        return len(result)
    
    except sqlite3.Error as e:
        print(f"Error @ {e}")
        return None
    
    except IOError as e:
        print(f"Another error @ {e}")
        return None

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Extracting data")
    records = extract_data(DB_FILE, OUTPUT_FILE)
    print(f"Extracted {records} records")
