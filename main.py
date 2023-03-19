import requests
import pprint
import json

from helpers.globals import *
from helpers.common import *
from helpers.category import *
from helpers.friends import *
from helpers.groups import *

# print(auth_dict)
pp = pprint.PrettyPrinter(indent=2)

clear()
print("Splitwise to Toshl expense transfer tool\n")
print("Loading config... ")

print("done")

auth_passed = True

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
print(f'  Toshl account: {user_accounts["toshl"]["email"]} ({user_accounts["toshl"]["id"]})' )
print("\n")
input("Press Enter to continue...")

while (True):
  clear()
  print("Splitwise to Toshl expense transfer tool\nMain Menu\n")
  print(f'  Splitwise account: {user_accounts["splitwise"]["email"]} ({user_accounts["splitwise"]["id"]})' )
  print(f'  Toshl account: {user_accounts["toshl"]["email"]} ({user_accounts["toshl"]["id"]})' )
  print("")
  print("What would you like to do now?")
  print("[1] Transfer from Friends List")
  print("[2] Transfer from Groups List")
  print("[0] Quit")
  i = input()
  if (i == '1'):
    friend_transfer_page()
  elif (i == '2'):
    group_transfer_page()
  elif (i == '0'):
    exit()
  else:
    print("Invalid input!")

  input("Press Enter to continue...")
  
