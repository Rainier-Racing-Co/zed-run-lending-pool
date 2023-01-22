import requests
import pandas as pd
from pandas import json_normalize
import backoff

@backoff.on_exception(backoff.expo, Exception, max_tries=8)
def get_summary_horse_data(horse_id):
    
    base_url = "https://zed-ql.zed.run/graphql"

    query = """
    query($input: HorseInput) {
        horse(input: $input) {
            name
            nft_id
            img_url
            gen
            bloodline
            breed_type
            color
            inserted_at
            super_coat
            horse_type
            race_statistic {
                first_place_finishes
                second_place_finishes
                third_place_finishes
                number_of_races
                win_rate
                number_of_free_races
                number_of_paid_races
                free_win_rate
                paid_win_rate
            }
            parents{
                name
                nft_id
            }
        }
    }
    """

    variables = {
        "input": {
            "horse_id": horse_id
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "query": query,
        "variables": variables
    }

    # Execute the POST query to GraphQL endpoint
    response = requests.post(base_url, json=payload, headers=headers)
    # print(response.status_code)

    # Transform data into json format
    summary_horse_data = response.json()
    
    # flattens json
    summary_horse_data = pd.json_normalize(summary_horse_data)

    return summary_horse_data

@backoff.on_exception(backoff.expo, Exception, max_tries=8)
def get_horse_data(horse_id):
    base_url = 'https://api.zed.run/api/v1/races/horse_stats'

    payload = {
        "content-type": "application/json"
    }

    variables = {
        "horse_id": horse_id
    }

    response = requests.get(base_url, json=payload, params=variables)

    response_json = response.json()

    flat_response = json_normalize(response_json)
    return flat_response

if __name__ == '__main__':
    query_result = get_summary_horse_data(8919)
    print(query_result)
