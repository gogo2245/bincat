import json
from code import run

config_file = open('config.json')
config = json.load(config_file)
config_file.close()
run(config)