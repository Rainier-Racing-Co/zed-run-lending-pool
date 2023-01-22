import requests
import pandas as pd
from modules.query_summary_horse_data import get_summary_horse_data
import backoff
from dotenv import load_dotenv
import os
import sys
import time

load_dotenv()
api_key = os.getenv("POLYSCAN_API_KEY")


@backoff.on_exception(backoff.expo, Exception, max_tries=8)

def query_lending_barn(page=1, offset=100):

    url = "https://api.polygonscan.com/api"

    params = {
        "module": "account",
        "action": "tokennfttx",
        "contractaddress": "0x67f4732266c7300cca593c814d46bee72e40659f",
        "address": "0x96016d03cb47e289b777eaabcf3b34a04bc54ae8",
        "startblock": 0,
        "endblock": 99999999,
        "page": page,
        "offset": offset,
        "sort": "desc",
        "apikey": api_key
    }

    response = requests.get(url, params=params)

    data = response.json()
    return data

if __name__ == '__main__':
    
    lending_barn = pd.DataFrame(columns=['Horse ID'])
    page = 1
    offset = 100
    
    while True:
        try:
            query_response = query_lending_barn(page, offset)
            query_results = query_response['result']
            
            horse_ids = [horse_id.get('tokenID') for horse_id in query_results]

            for id in horse_ids:
                # horse_data_obj = get_summary_horse_data(int(id))
                lending_barn = lending_barn.append({'horse_id': int(id)}, ignore_index=True)
                lending_barn.to_csv('data/lending_barn.csv')
                time.sleep(0.1)
                print(f"Horses: {len(lending_barn.index)}, Page: {page}")
                
            if len(horse_ids) < offset:
                break
            
            time.sleep(0.1)
            page += 1
        except KeyboardInterrupt:
            print("\nScript interrupted by user. Exiting...")
            sys.exit()
        except:
            time.sleep(30)
            continue
