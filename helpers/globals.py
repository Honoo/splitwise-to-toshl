import configparser

toshl_category_tag = {} # Contains categories keyed by id, and tags
toshl_categories = [] # Contains categories sorted by usage
toshl_tags = [] # Contains tags sorted by usage

config = configparser.RawConfigParser()
config.read('config.cfg')
auth_dict = dict(config.items('API_KEYS'))


splitwise_headers = {"content-type":"application/json", "Authorization": "Bearer " + auth_dict['splitwise_api_key']}
toshl_headers = {"content-type":"application/json", "Authorization": "Bearer " + auth_dict['toshl_api_key']}

user_accounts = {}
