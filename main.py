import configparser
import requests
import pprint
import json

# print(auth_dict)


print("Splitwise to Toshl expense transfer tool\n")
print("\n")
print("Loading config... ")

config = configparser.RawConfigParser()
config.read('config.cfg')
auth_dict = dict(config.items('API_KEYS'))
print("done\n")


auth_passed = True
user_accounts = {}
print("Checking splitwise token... ")
r = requests.get('https://secure.splitwise.com/api/v3.0/get_current_user', headers={"content-type":"application/json", "Authorization": "Bearer " + auth_dict['splitwise_api_key']})

if (r.status_code == 200):
  print("success")
  user_obj = json.loads(r.text)
  # print(user_obj)
  user_accounts['splitwise'] = user_obj['user']['email']
else:
  print(r.text)
  auth_passed = False

print("Checking toshl token... ")
r = requests.get("https://api.toshl.com/me", headers={"content-type":"application/json", "Authorization": "Bearer " + auth_dict['toshl_api_key']})
if (r.status_code == 200):
  print("success")
  user_obj = json.loads(r.text)
  # print(user_obj)
  user_accounts['toshl'] = user_obj['email']
else:
  print(r.text)
  auth_passed = False


if not auth_passed:
  print('There are errors with the authorisation code, please check your config')
  exit()

print('Successfully authenticated with both services.')
print('  Splitwise account: ' + user_accounts['splitwise'])
print('  Toshl account:     ' + user_accounts['toshl'])

