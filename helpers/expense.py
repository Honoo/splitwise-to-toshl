import requests
import json

from .category import *
from .common import *

def add_expense(breadcrumb, expense):
  e = expense
  
  bail, selected_category = get_category(breadcrumb, expense)
  if bail:
    return True  # Break out of expense page loop

  bail, selected_tag = get_tag(breadcrumb, expense, selected_category)
  if bail:
    return True  # Break out of expense page loop

  # Add the entry to toshl
  data = {
    "amount": -abs(float(e['share_amount'])),
    "currency": { "code": e['currency'] },
    "date": e['date'],
    "desc": e['description'],
    "category": selected_category['id'],
    "extra": {
      "friends": e['friends']
    }
  }
  if selected_tag is not None:
    data['tags'] = [selected_tag['id']]
  r = requests.post(f"https://api.toshl.com/entries", data=json.dumps(data), headers=toshl_headers)
  if r.status_code == 201:
    print("Successfully added expense:")
    print(toshl_entry_short_string(data))
  else:
    print("Could not add expense:")
    print(f"Status: {r.status_code}")
    print(r.text)

  input("Press Enter to continue")
  return False