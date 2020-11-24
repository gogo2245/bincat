from googleapiclient.discovery import build
import json

config_file = open('config.json')
config = json.load(config_file)
config_file.close()

my_api_key = config['google_api_key']
my_cse_id = config['google_cse_id']

queries = config['queries']
formats = config['formats']


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

response = {}

for f in formats:
    for q in queries:
        results = google_search(
            q, my_api_key, my_cse_id, searchType='image', fileType=f, num=10)
        results = list(map(lambda item: item['link'], results))
        if f not in response:
            response[f] = results
        else:
            response[f] += results

f = open('imageUrls.json', 'w')
f.write(json.dumps(response))
f.close()
