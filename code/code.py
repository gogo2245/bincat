from github import Github
import json

config_file = open('config.json')
config = json.load(config_file)
config_file.close()

github = Github(config['github_access_key'])
max_repos = config['max_repos']

repos = github.get_repos()
clone_urls = {}
i = 0
for repo in repos:
    if i == max_repos:
        break
    lang = repo.language
    clone_url = repo.clone_url
    if lang not in clone_urls:
        clone_urls[lang] = [clone_url]
    else:
        clone_urls[lang].append(clone_url)

    i += 1

f = open('cloneUrls.json', 'w')
f.write(json.dumps(clone_urls))
f.close()
