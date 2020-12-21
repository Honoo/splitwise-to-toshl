import configparser
import requests
import pprint
import json
from datetime import datetime, timedelta
from os import system, name

# print(auth_dict)
pp = pprint.PrettyPrinter(indent=2)

# Take a date string and output the previous day and next day as strings
# e.g. input: "2020-05-20"
#      output: ["2020-05-19", "2020-05-21"]
def get_date_buffer(date_str):
  dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
  upper_date = dt_obj + timedelta(days=1)
  upper = upper_date.strftime("%Y-%m-%d")
  lower_date = dt_obj - timedelta(days=1)
  lower = lower_date.strftime("%Y-%m-%d")
  return [lower, upper]

def clear():
  if name == 'nt':
    _ = system('cls')
  # for mac and linux(here, os.name is 'posix')
  else:
    _ = system('clear')


toshl_category_tag = {} # Contains categories keyed by id, and tags
toshl_categories = [] # Contains categories sorted by usage
toshl_tags = [] # Contains tags sorted by usage

def get_toshl_cats_and_tags():
  r = requests.get("https://api.toshl.com/categories", headers=toshl_headers)
  cat_response = json.loads(r.text)
  # Sort by number of entries per category
  cat_response = sorted(cat_response, key=lambda x:-x['counts']['entries'] )
  
  for c in cat_response:
    if not c['deleted'] and c['type'] == 'expense':
      cat = {
        'id': c['id'],
        'name': c['name'],
        'tags': []
      }
      toshl_categories.append(cat)
      toshl_category_tag[c['id']] = cat

  r = requests.get("https://api.toshl.com/tags", headers=toshl_headers)
  tag_response = json.loads(r.text)
  # Sort by number of entries per category
  tag_response = sorted(tag_response, key=lambda x:-x['counts']['entries'] )
  for t in tag_response:
    if not t['deleted'] and t['type'] == 'expense':
      tag = {
        'id': t['id'],
        'name': t['name'],
        'category': t['category']
      }
      toshl_tags.append(tag)
      if tag['category'] in toshl_category_tag:
        toshl_category_tag[tag['category']]['tags'].append(tag)


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

def get_friend_expenses(friend_id, count, page):
  r = requests.get(f'https://secure.splitwise.com/api/v3.0/get_expenses?friend_id={friend_id}&limit={count}&offset={page * count}', headers=splitwise_headers)
  involved_expenses_arr = []
  expenses_arr = json.loads(r.text)['expenses']
  for e in expenses_arr:
    expense = {
      "category": e['category']['name'],
      "description": e['description'],
      "currency" : e['currency_code'],
      "total_amount" : float(e['cost']),
      "date" : e['date'].split('T')[0] ,
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
  return involved_expenses_arr

def splitwise_expense_short_string(e):
  return f"{e['date']} {e['share_amount']} {e['currency']}\t[{e['category']}] - {e['description']}"

def splitwise_expense_long_string(e):
  return f"{e['date']}\n{e['share_amount']} {e['currency']} (total: {e['total_amount']} {e['currency']})\n[{e['category']}]\n{e['description']}"


def toshl_entry_short_string(e):
  cat_id = e['category']
  category = toshl_category_tag[cat_id]['name']
  description = e['desc'].replace('\n', ' ').replace('\r', '')
  if len(description) > 50:
    description = f"{description[0:50]} ..."
  return f"{e['date']} {abs(e['amount'])} {e['currency']['code']} [{category}] - {description}"


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

print("Checking toshl token... ")
r = requests.get("https://api.toshl.com/me", headers=toshl_headers)
if (r.status_code == 200):
  print("success")
  user_obj = json.loads(r.text)
  # print(user_obj)
  user_accounts['toshl'] = {}
  user_accounts['toshl']['email'] = user_obj['email']
  user_accounts['toshl']['id'] = user_obj['id']
else:
  print(r.text)
  auth_passed = False

print("Loading toshl categories and tags... ")
get_toshl_cats_and_tags()
print("success")


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
    clear()
    print(f"Friend Transfer ") 
    print(f"==========================================") 
    print("")
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
        print('Invalid input!')
        input("Press Enter to try again")
      else:
        selected_friend = friends_with_balances[int(i)]
        break

    
    page = 1
    while (True):
      clear()
      full_name = ' '.join(filter(None, (selected_friend['first_name'], selected_friend['last_name'])))
      print(f"Friend Transfer > {full_name} > Page {page}") 
      print(f"==========================================") 
      print("")
      print("Loading expenses for " + full_name + "\n")

      expenses = get_friend_expenses(selected_friend["id"], 10, page - 1)

      # Give users some UI to decide what expenses they want.
      if len(expenses) == 0:
        print("There were no expenses here, you can try loading the next page")
      else:
        print("Here is what we found:")
        for e in expenses:
          print("   " + splitwise_expense_short_string(e))

      print("")
      print("Choose an option")
      print("1. Start processing here (you can skip individual expenses)")
      print("2. Load next page")
      print("0. Back to main menu")

      i = input()
      if (i == '1'):
        expense_ind = 1
        for e in expenses:
          clear()
          print(f"Friend Transfer > {full_name} > Page {page} > Item {expense_ind} of {len(expenses)}") 
          print(f"==========================================") 
          print("")
          print(splitwise_expense_long_string(e))
          print("")

          dates = get_date_buffer(e['date'])
          print(f"Checking for similar expenses on Toshl from {dates[0]} to {dates[1]}")
          # Check toshl for similar expenses
          r = requests.get(f"https://api.toshl.com/entries?type=expense&from={dates[0]}&to={dates[1]}", headers=toshl_headers)
          toshl_entries = json.loads(r.text)
          similar_entries = []
          for te in toshl_entries:
            # If it has roughly the same price
            # If it has the same description
            similar_price = abs(abs(abs(te['amount']) - abs(float(e['share_amount'])) / abs(te['amount']))) < 0.2
            toshl_description = te['desc'].replace('\n', ' ').replace('\r', '').replace(' ', '')
            spliwise_description = e['description'].replace('\n', ' ').replace('\r', '').replace(' ', '')
            similar_description = toshl_description == spliwise_description
            if similar_price or similar_description:
              similar_entries.append(te)
          if len(similar_entries) == 0:
            print("   No similar expenses found")
          else:
            print(f"   Found {len(similar_entries)} similar expenses:")
            for se in similar_entries:
              print(f'    - {toshl_entry_short_string(se)}')
          
          print("")
          # Give options to add, or skip
          print("Choose an option")
          print("1. Add expense (you need to provide the category and tags)")
          print("2. Skip expense")
          print("0. Finish this page and go back")

          i = input()
          if (i == '1'):
            # Get toshl categories
            # Get toshl tags
            expense_ind += 1
            continue
          elif (i == '2'):
            expense_ind += 1
            continue
          elif (i == '0'):
            break
          else:
            print('Invalid input!')
            input("Press Enter to try again")

        
        page += 1
        continue
      elif (i == '2'):
        page += 1
        continue
      elif (i == '0'):
        break
      else:
        print('Invalid input!')
        input("Press Enter to try again")

    

      
  elif (i == '0'):
    exit()
  else:
    print("Invalid input!")

  input("Press Enter to continue...")
  
