import os
import requests
from dotenv import load_dotenv

load_dotenv()

URL_ENDPOINT = os.getenv("URL_ENDPOINT")

def wei_to_bnb(wei):
    return(int(wei, 16)/ 10**18)

def check_transaction_status(tx_hash):

    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getTransactionReceipt",
        "params": [tx_hash],
        "id": 1,
    }

    headers = { "Content-Type": "application/json" }

    try: 
        response = requests.post(URL_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        
        if 'error' in response_json:
            print(f"API Error: {response_json['error']['message']}")
            return
        
        receipt = response_json.get('result')

        if not receipt:
            print("No transaction found") # result: None
            return
        
        for log in receipt.get('logs', []): # BEP20 

            if log['topics'][0] == '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef':
                token_contract = log['address']
                token_value_raw = int(log['data'], 16)
                token_value_human = token_value_raw / (10**18) 
                
                print(f"BEP-20 Transfer Found:")
                print(f"Amount: {token_value_human} tokens")
                print(f"Token Contract: {token_contract}")
                break # Assume only one transfer

        status_hex = receipt.get('status')
        status = "Success" if status_hex == '0x1' else "Failed"

        tx_payload = {
            "jsonrpc": "2.0",
            "method": "eth_getTransactionByHash",
            "params": [tx_hash],
            "id": 1,
        }

        tx_response = requests.post(URL_ENDPOINT, json=tx_payload, headers=headers)
        tx_details = tx_response.json()['result']
        value = wei_to_bnb(tx_details['value'])

        print(f"\nTransaction details:")
        print(f"Status:{status}")
        print(f"Block Number: {int(receipt.get('blockNumber'), 16)}")
        print(f"From Address: {receipt.get('from')}")
        print(f"To Address: {receipt.get('to')}")
        print(f"Value: {value:.6f} BNB")

        gas_used = int(receipt.get('gasUsed'), 16)
        gas_price = int(tx_details.get('gasPrice'), 16)

        transaction_fee_wei = gas_used * gas_price
        transaction_fee_bnb = transaction_fee_wei / (10**18)

        print(f"Transaction Fee: {transaction_fee_bnb:.8f} BNB")

    except requests.exceptions.RequestException as e:
        print(f"Error: bad API request: {e}")
    except KeyError as e:
        print(f"Error: Missing key: {e}")
    except Exception as e:
        print(f"Error: Unexpected: {e}")

if __name__ == "__main__":
    test_tx_hash = "0x9e976cf3f916787dd92695e6c1c22eb729d2bf614b5e2b61ccdc8b9cf79bf76f"
    check_transaction_status(test_tx_hash)