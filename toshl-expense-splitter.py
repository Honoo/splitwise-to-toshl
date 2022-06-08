# This program splits the toshl expenses into multiple parts.

from os import system, name
import configparser
from re import L
import requests
import pprint
import json
import csv
from datetime import datetime, timedelta

toshl_category_tag = {} # Contains categories keyed by id, and tags
toshl_categories = [] # Contains categories sorted by usage
toshl_tags = [] # Contains tags sorted by usage
toshl_category_hash = {} # Contains categories keyed by id
toshl_tag_hash = {} # Contains tags keyed by id


def clear():
  if name == 'nt':
    _ = system('cls')
  # for mac and linux(here, os.name is 'posix')
  else:
    _ = system('clear')


treat_category_id = '866019'
rachel_tag_id = '66472251'

def get_toshl_cats_and_tags():
  r = requests.get("https://api.toshl.com/categories?per_page=500", headers=toshl_headers)
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
      toshl_category_hash[c['id']] = c['name']
      toshl_categories.append(cat)
      toshl_category_tag[c['id']] = cat

  r = requests.get("https://api.toshl.com/tags?per_page=500", headers=toshl_headers)
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
      toshl_tag_hash[t['id']] = t['name']
      toshl_tags.append(tag)
      if tag['category'] in toshl_category_tag:
        toshl_category_tag[tag['category']]['tags'].append(tag)

def split_expense(entry):
  e = entry
  truncated_desc = e['desc'].replace("\n", ' ')[0:30]
  print("Processing entry:")
  print(f"{e['date']} \t ${abs(e['amount'])}\t {truncated_desc}")
  print(f"\tCat: {toshl_category_hash[e['category']]}\t   Tags: {','.join(tag_list)}")
  print("")

  # Split the entry into two parts
  split_amount_30 = -round(abs(e['amount']) * 100 * 0.3) / 100
  split_amount_70 = -round((abs(e['amount']) + split_amount_30) * 100) / 100

  e['tags']

  new_tags = e['tags'].copy()
  new_tags.append(rachel_tag_id)
  data = {
    "amount": split_amount_30,
    "currency": { "code": "USD" },
    "date": e['date'],
    "desc": e['desc'],
    "category": treat_category_id,
    "tags": new_tags,
    "account": e['account'],
    "split": {
      "parent": e['id']
    }
  }

  data2 = {
    "amount": split_amount_70,
    "currency": { "code": "USD" },
    "date": e['date'],
    "desc": e['desc'],
    "category": e['category'],
    "tags": e['tags'],
    "account": e['account'],
    "split": {
      "parent": e['id']
    }
  }

  print("Creating split with these two entries:")

  # pp.pprint(data)
  # pp.pprint(data2)
  # if (input("Enter y to continue") != "y"):
  #   input("Cancelled. Press enter to continue")
  #   return

  r = requests.post(f"https://api.toshl.com/entries?immediate_update=true", data=json.dumps(data), headers=toshl_headers)
  if r.status_code == 201:
    print("Successfully added split 1")
  else:
    print("Could not add expense:")
    print(f"Status: {r.status_code}")
    print(r.text)

  r = requests.post(f"https://api.toshl.com/entries?immediate_update=true", data=json.dumps(data2), headers=toshl_headers)
  if r.status_code == 201:
    print("Successfully added split 2")
  else:
    print("Could not add expense:")
    print(f"Status: {r.status_code}")
    print(r.text)

  print("Done")

  input("Press Enter to continue...")

pp = pprint.PrettyPrinter(indent=2)

config = configparser.RawConfigParser()
config.read('config.cfg')
auth_dict = dict(config.items('API_KEYS'))

toshl_headers = {"content-type":"application/json", "Authorization": "Bearer " + auth_dict['toshl_api_key']}

auth_passed = True
user_accounts = {}
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
# pp.pprint(toshl_tags)



date_iterator = datetime.now()
page = 0

while(True):
  clear()
  print("Toshl Expense Splitter")
  print("========================")
  to_date = date_iterator.strftime("%Y-%m-%d")
  from_date = (date_iterator - timedelta(days=30)).strftime("%Y-%m-%d")
  print("Dates from " + from_date + " to " + to_date)
  print("Processing entries: " + str(page*10 + 1) + " to " + str((page+1)*10 + 1))


  r = requests.get(f"https://api.toshl.com/entries?type=expense&from={from_date}&to={to_date}&page={page}&per_page=20&!tags={rachel_tag_id}", headers=toshl_headers)
  # pp.pprint(r.text)
  toshl_entries = json.loads(r.text)

  # pp.pprint(toshl_entries[0:7])

  if len(toshl_entries) == 0:
    print("No more entries")
    print()
    print()
    print()
  else:
    iter = 1
    for e in toshl_entries:
      tag_list = []
      if 'tags' in e:
        for tag in e['tags']:
          if tag in toshl_tag_hash:
            tag_list.append(toshl_tag_hash[tag])
          else:
            # print("Tag not found: " + tag)
            pass
      truncated_desc = e['desc'].replace("\n", ' ')[0:30]
      friends = ""
      # Check if key extra exists
      if 'extra' in e:
        friends = e['extra']['friends']
      if ('category' in e):
        print(f"[{iter}]\t{e['date']} \t ${abs(e['amount'])}\t {truncated_desc} \t {friends}")
        print(f"\tCat: {toshl_category_hash[e['category']]}\t   Tags: {','.join(tag_list)}")
      iter += 1




  print("\n")
  print("[n] Process item")
  print("[<] Previous page [>] Next page")
  print("[<<] Previous month [>>] Next month")

  i = input()
  
  if i == "<":
    page -= 1
    if page < 0:
      page = 0
  elif i == ">":
    page += 1
  elif i == "<<":
    date_iterator = date_iterator - timedelta(days=30)
    page = 0
  elif i == ">>":
    date_iterator = date_iterator + timedelta(days=30)
    page = 0
  else:
    input_integer = int(i)
    if input_integer > 0 and input_integer <= len(toshl_entries):
      print("Processing entry: " + str(input_integer))
      entry = toshl_entries[input_integer-1]
      split_expense(entry)
    else:
      print("Invalid input")
      input("Press enter to continue...")
