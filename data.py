import pandas as pd
import requests
import time
from datetime import datetime

information_for_dataframe = {
    'id': [],
    'text': [],
    'likes': [],
    'comments': [],
    'views': [],
    'reposts': [],
    'photo': [],
    'url': [],
    'date': [],
    'date_UNIX': []
}

url_start = 'https://vk.com/nenovijukabachki'
url = url_start.split('/')
access_token = "0f081c180f081c180f081c18270c1f36aa00f080f081c186aca12d5e53fc3d7df54f2af"
version = 5.199
domain = url[-1]
count = 100
offset = 0

response = requests.get('https://api.vk.com/method/wall.get',
                        params={'access_token': access_token,
                                'v': version,
                                'domain': domain,
                                'count': count,
                                'offset': offset
                                })

data_start = response.json()
response = requests.get('https://api.vk.com/method/utils.resolveScreenName',
                        params={'access_token': access_token,
                                'screen_name': domain,
                                'v': version
                                })
id_group = response.json()['response']['object_id']
count_posts = data_start['response']['count']

for i in range(0, count_posts, 100):
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={'access_token': access_token,
                                    'v': version,
                                    'domain': domain,
                                    'count': count,
                                    'offset': offset
                                    })
    data = response.json()['response']['items']
    offset += 100
    information_for_dataframe['id'].extend([item['id'] for item in data])
    information_for_dataframe['likes'].extend([item['likes']['count'] for item in data])
    information_for_dataframe['text'].extend([item['text'] for item in data])
    information_for_dataframe['comments'].extend([item['comments']['count'] for item in data])
    information_for_dataframe['views'].extend([item['views']['count'] for item in data])
    information_for_dataframe['reposts'].extend([item['reposts']['count'] for item in data])
    information_for_dataframe['photo'].extend([item['attachments'][0]['photo']['sizes'][-1]['url'] if len(item.get('attachments', [])) > 0 else "No photo" for item in data])
    information_for_dataframe['url'].extend([url_start + "?w=wall-" + str(id_group) +"_"+ str(item['id']) for item in data])
    from datetime import datetime, timezone

    information_for_dataframe['date'].extend(
        [datetime.fromtimestamp(item['date'], timezone.utc).strftime('%Y-%m-%d %H:%M:%S') for item in data])

    information_for_dataframe['date_UNIX'].extend([item['date'] for item in data])
    time.sleep(0.1)

df = pd.DataFrame(information_for_dataframe)
print(df.head())

pd.set_option('display.max_columns', None)
print(df.head(3))
