import requests, json, yaml


def get_access_token():
    
    with open(f'key.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        
    headers = {"content-type":"application/json"}
    body = {"grant_type":"client_credentials",
            "appkey":config['APP_KEY'], 
            "appsecret":config['APP_SECRET']}

    PATH = "oauth2/tokenP"
    URL = f"{config['URL_BASE']}/{PATH}"

    res = requests.post(URL, headers=headers, data=json.dumps(body))
    ACCESS_TOKEN = res.json()["access_token"]
    config['ACCESS_TOKEN'] = ACCESS_TOKEN
    
    with open(f'key.yaml', 'w') as file:
        yaml.dump(config, file)
    
    return ACCESS_TOKEN


if __name__ == '__main__':
    
    print('Access token: \n')
    print(get_access_token())

