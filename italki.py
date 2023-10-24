# Imports the italki expenses into toshl

from os import system, name
import configparser
import requests
import pprint
import json
import csv
from datetime import datetime, timedelta

toshl_category_tag = {} # Contains categories keyed by id, and tags
toshl_categories = [] # Contains categories sorted by usage
toshl_tags = [] # Contains tags sorted by usage
italki_entries = {} # Contains entries from italki

jap_lesson_id = 16390095
italki_id = 29550265
education_id = 866018

def get_all_italki_entries():
  r = requests.get(f"https://api.toshl.com/entries?type=expense&from=2000-01-01&to=2022-01-01&tags=29550265", headers=toshl_headers)
  italki_response = json.loads(r.text)
  for entry in italki_response:
  italki_entries[entry['date']] = entry

def toshl_entry_short_string(e):
  cat_id = e['category']
  category = toshl_category_tag[cat_id]['name']
  description = e['desc'].replace('\n', ' ').replace('\r', '')
  if len(description) > 50:
  description = f"{description[0:50]} ..."
  return f"{e['date']} {abs(e['amount'])} {e['currency']['code']} [{category}] - {description}"


def add_to_toshl(prev_row, total_day_amount):
  date = datetime.strptime(prev_row['date'], '%d %b %Y').strftime('%Y-%m-%d')
  # print(date + " " + str(total_day_amount))
  if date in italki_entries:
  print("Found entry for date: " + date + " " + str(total_day_amount) + " " + str(italki_entries[date]['amount']))
  else:
  print("Adding entry for date " + date + " " + str(total_day_amount))
  data = {
  "amount": -abs(float(total_day_amount)),
  "currency": { "code": "USD" },
  "date": date,
  "desc": prev_row['teacher'].capitalize(),
  "category": education_id,
  "tags": [jap_lesson_id, italki_id]
  }

  r = requests.post(f"https://api.toshl.com/entries", data=json.dumps(data), headers=toshl_headers)
  if r.status_code == 201:
  print("Successfully added expense for: " + date + " " + str(total_day_amount))
  else:
  print("Could not add expense:")
  print(f"Status: {r.status_code}")
  print(r.text)
  


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

get_all_italki_entries()
# 
# pp.pprint(italki_entries)

with open('italki.csv', newline='') as csvfile:
  lesson_reader = csv.DictReader(csvfile)
  total_day_amount = 0
  prev_row = {}
  for row in lesson_reader:
  if prev_row == {}:
  total_day_amount += float(row['cost'])
  elif row['date'] == prev_row['date'] and row['teacher'] == prev_row['teacher']:
  total_day_amount += float(row['cost'])
  else:
  add_to_toshl(prev_row, total_day_amount)

   
  total_day_amount = float(row['cost'])
  prev_row = row

  add_to_toshl(prev_row, total_day_amount)
  
