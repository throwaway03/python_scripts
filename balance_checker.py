from dotenv import load_dotenv
import os
import csv
import time
import requests

load_dotenv()

URL_ENDPOINT = os.getenv("URL_ETH_ENDPOINT")

def wei_to_eth(wei):
    return int(wei, 16) / 10**18

def get_address_balance(address, URL_ENDPOINT):
    
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"], #most recent block?
        "id": 1,
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(URL_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        response_json = response.json()

        if 'error' in response_json:
            print(f"Something bad happened @ {address}")
            return None
        
        balance_wei = response_json.get('result')
        if balance_wei is not None:
            return wei_to_eth(balance_wei)
        else: return None

    except response.exceptions.RequestException as e:
        print(f"Bad request: {e}")
        return None
    except Exception as e:
        print(f"Error at {address} -- {e}")
        return None
    
def process_addresses(input_file, output_file):
    URL_ENDPOINT = os.getenv("URL_ENDPOINT")

    try:
        with open(input_file, 'r') as f_in:
            addresses = [line.strip() for line in f_in if line.strip()]
    except FileNotFoundError:
        print(f"No file found - {f_in}")
        return
    
    with open(output_file, 'w') as f_out:
        csv_writer = csv.writer(f_out)
        csv_writer.writerow(['address', 'balance_eth'])

        total = len(addresses)
        for i, address in enumerate(addresses):
            print(f"Procressing adresses: {i+1}/{total}: {address}")

            balance = get_address_balance(address, URL_ENDPOINT)

            if balance is not None:
                csv_writer.writerow([address, f"{balance:.18f}"])
            else: 
                csv_writer.writerow([address, 'Error'])

        time.sleep(0.2)

if __name__ == "__main__":
    INPUT_FILE = 'addresses.txt'
    OUTPUT_FILE = 'balance.csv'
    print("Starting Balance Checker")
    process_addresses(INPUT_FILE, OUTPUT_FILE)
    print(f"Results have been saved to {OUTPUT_FILE}")
    
