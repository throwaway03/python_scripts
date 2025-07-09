import re

def find_user_errors(log_file_path,user_id):

    user_errors = []

    tx_id_pattern = re.compile(r"transaction_id:(\w+)")

    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                if "ERROR" in line and f"user_id:{user_id}" in line:
                    match = tx_id_pattern.search(line)
                    tx_id = match.group(1) if match else "N/A"

                    error_info = {
                        "user_id": user_id,
                        "transaction_id": tx_id,
                        "full_log_messsage": line.strip(),
                    }

                    user_errors.append(error_info)

    except FileNotFoundError:
        print(f"File not found")
        return []
    
    return user_errors 

if __name__ == "__main__":

    errors = find_user_errors("log.txt", 12345)
    print(errors)


