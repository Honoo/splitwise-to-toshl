from datetime import datetime, timedelta
from os import system, name

from .globals import *

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

def splitwise_expense_short_string(e):
  return f"{e['date']} {e['share_amount']} {e['currency']}\t[{e['category']}] - {e['description']}"

def splitwise_expense_long_string(e):
  return f"{e['date']}\nYour share: {e['share_amount']} {e['currency']} (Total: {e['total_amount']} {e['currency']})\n[{e['category']}]\n{e['description']}"


def toshl_entry_short_string(e):
  cat_id = e['category']
  category = toshl_category_tag[cat_id]['name']
  description = e['desc'].replace('\n', ' ').replace('\r', '')
  if len(description) > 50:
    description = f"{description[0:50]} ..."
  return f"{e['date']} {abs(e['amount'])} {e['currency']['code']} [{category}] - {description}"

def get_similar_toshl_entries(splitwise_entry, toshl_entries):
  e = splitwise_entry
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
  return similar_entries
