import requests

api_url = "https://prod-api.kosetto.com"
api_key = ""


def get_user(wallet):
    api = api_url + f"/users/{wallet}"
    response = requests.get(api).json()
    return response


def twitter_score(username):
    params = {
        'accountSlug': username,
    }
    r = requests.get('https://twitterscore.io/twitter/graph/ajax/', params=params).json()
    return r


if __name__ == '__main__':
    checked_transactions = []
    while True:
        api = "https://api.basescan.org/api"
        params = {
            "module": "account",
            "action": "txlist",
            "address": "0xcf205808ed36593aa40a44f10c7f7c2f67d4a4d4",
            "startblock": 4135015,
            "endblock": 99999999,
            "page": 1,
            "offset": 100,
            "sort": "desc",
            "apikey": api_key
        }
        r = requests.get(api, params=params).json()
        for transaction in r['result']:
            if transaction['hash'] not in checked_transactions:
                checked_transactions.append(transaction['hash'])
                if transaction['functionName'] == "buyShares(address sharesSubject,uint256 amount)" and transaction["value"] == "0":
                    # print(transaction)
                    # print(f"From: {transaction['from']}")
                    user = get_user(transaction['from'])
                    if "message" not in user:
                        print(user)
                        ts = twitter_score(user['twitterUsername'])
                        if len(ts['scores']) > 0:
                            print(user['twitterUsername'])
                            print(f"Followers: {ts['followers'][-1]['value']}")
                            print(f"Twitter score: {ts['scores'][-1]['value']}")
                            print("")
