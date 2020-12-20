import configparser
import requests
import pprint
import json
from os import system, name

# print(auth_dict)
pp = pprint.PrettyPrinter(indent=2)
def clear():
  if name == 'nt':
    _ = system('cls')
  # for mac and linux(here, os.name is 'posix')
  else:
    _ = system('clear')

clear()
print("Splitwise to Toshl expense transfer tool\n")
print("\n")
print("Loading config... ")

config = configparser.RawConfigParser()
config.read('config.cfg')
auth_dict = dict(config.items('API_KEYS'))
print("done\n")
splitwise_headers = {"content-type":"application/json", "Authorization": "Bearer " + auth_dict['splitwise_api_key']}
toshl_headers = {"content-type":"application/json", "Authorization": "Bearer " + auth_dict['toshl_api_key']}

auth_passed = True
user_accounts = {}
print("Checking splitwise token... ")
r = requests.get('https://secure.splitwise.com/api/v3.0/get_current_user', headers=splitwise_headers)

if (r.status_code == 200):
  print("success")
  user_obj = json.loads(r.text)
  # print(user_obj)
  user_accounts['splitwise'] = {}
  user_accounts['splitwise']['email'] = user_obj['user']['email']
  user_accounts['splitwise']['id'] = user_obj['user']['id']
else:
  print(r.text)
  auth_passed = False

# print("Checking toshl token... ")
# r = requests.get("https://api.toshl.com/me", headers=toshl_headers)
# if (r.status_code == 200):
#   print("success")
#   user_obj = json.loads(r.text)
#   # print(user_obj)
#   user_accounts['toshl'] = {}
#   user_accounts['toshl']['email] = user_obj['email']
#   user_accounts['toshl']['id] = user_obj['id']
# else:
#   print(r.text)
#   auth_passed = False


# if not auth_passed:
#   print('There are errors with the authorisation code, please check your config')
#   exit()

print('Successfully authenticated with both services.')
print(f'  Splitwise account: {user_accounts["splitwise"]["email"]} ({user_accounts["splitwise"]["id"]})' )
# print(f'  Toshl account: {user_accounts["toshl"]["email"]} ({user_accounts["toshl"]["id"]})' )
# print("\n")
# input("Press Enter to continue...")

while (True):
  # clear()
  print("What would you like to do now?")
  print("1. Transfer from Friends List")
  print("0. Quit")
  i = input()
  if (i == '1'):
    print("Loading friends list:")
    r = requests.get('https://secure.splitwise.com/api/v3.0/get_friends', headers=splitwise_headers)
    friends_arr = json.loads(r.text)['friends']
    print("Which friend's expenses do you want to sync?")
    friends_with_balances = []
    ind = 0
    for f in friends_arr:
      if ( len(f['balance']) > 0):
        full_name = ', '.join(filter(None, (f['first_name'], f['last_name'])))
        print(str(ind) + '. ' + full_name + ' ' + f['balance'][0]['amount'] + f['balance'][0]['currency_code'])
        friends_with_balances.append(f)
        ind = ind +1

    selected_friend = None
    while(True):
      i = input()
      if (int(i) < 0 or int(i) >= len(friends_with_balances)):
        print('Invalid selection!')
      else:
        selected_friend = friends_with_balances[int(i)]
        break

    full_name = ' '.join(filter(None, (selected_friend['first_name'], selected_friend['last_name'])))
    print("Loading 20 expenses for " + full_name)

    r = requests.get(f'https://secure.splitwise.com/api/v3.0/get_expenses?friend_id={selected_friend["id"]}&limit=5', headers=splitwise_headers)
    involved_expenses_arr = []
    expenses_arr = json.loads(r.text)['expenses']
    for e in expenses_arr:
      expense = {
        "category": e['category']['name'],
        "description": e['description'],
        "currency" : e['currency_code'],
        "total_amount" : float(e['cost']),
        "date" : e['date'],
        "share_amount" : 0
      }
      expense_users = e['users']
      for eu in expense_users:
        if eu['user_id'] == user_accounts['splitwise']['id']:
          expense['share_amount'] = float(eu['owed_share'])
          break

      if expense['share_amount'] > 0:
        involved_expenses_arr.append(expense)
        # pp.pprint(expense)

    for e in involved_expenses_arr:
      pp.pprint(e)
      
  elif (i == '0'):
    exit()
  else:
    print("Invalid input, try again.")

  input("Press Enter to continue...")
  
    