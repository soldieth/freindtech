import requests
import json
api_url = "https://prod-api.kosetto.com"


def get_user(user_id):
    api = api_url + "/users/by-id/"
    response = requests.get(f"{api}+{user_id}").json()
    return response


def twitter_score(username):
    params = {
        'accountSlug': username,
    }
    r = requests.get('https://twitterscore.io/twitter/graph/ajax/', params=params).json()
    return r


if __name__ == '__main__':
    with open("config.json", "r") as file:
        config = json.load(file)
    user_id = int(config['start_user_id'])
    try:
        while True:
            r = get_user(user_id)
            if "message" not in r:
                twitter_username = r['twitterUsername']
                user_id += 1
                config['start_user_id'] = user_id
                ts = twitter_score(twitter_username)
                if len(ts['scores']) > 0:
                    print(r)
                    print(f"Followers: {ts['followers'][-1]['value']}")
                    print(f"Twitter score: {ts['scores'][-1]['value']}")
                else:
                    print("Дерьмо аккаунт")
    finally:
        with open("config.json", "w") as file:
            file.write(json.dumps(config))

