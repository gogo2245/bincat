import wikipedia
import json

config_file = open('config.json')
config = json.load(config_file)
config_file.close()

langs = config['langs']
texts = config['queries']

results = {}

for l in langs:
    wikipedia.set_lang(l)
    for t in texts:
        result = wikipedia.search(t, results=10)
        for r in result:
            page = None
            try:
                page = wikipedia.page(r)
            except wikipedia.exceptions.DisambiguationError as e:
                if 0 in e.options:
                    try:
                        page = wikipedia.page(e.options[0])
                    except e:
                        print(e)
            except wikipedia.exceptions.PageError as e:
                print(e)
            if page is None:
                continue
            if l not in results:
                results[l] = [page.content]
            else:
                results[l].append(page.content)

f = open('text.json', 'wb')
f.write(json.dumps(results, ensure_ascii=False).encode('utf8'))
f.close()
