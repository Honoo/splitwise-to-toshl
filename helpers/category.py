import requests
import json

from .common import *
from .globals import *

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
      toshl_tags.append(tag)
      if tag['category'] in toshl_category_tag:
        toshl_category_tag[tag['category']]['tags'].append(tag)

def get_category(breadcrumb, expense):
  bail = False
  finish = False
  offset = 0
  page_size = 10
  selected_category = None
  while(True): # Paginate category list
    clear()
    print(f"{breadcrumb} > Add Expense > Choose Category") 
    print(f"==========================================") 
    print("")
    print("Adding expense:")
    print(splitwise_expense_long_string(expense))
    print("")
    print(f"Choose your category (showing {offset+1} to {offset+page_size+1})")
    
    ind = 0
    toshl_categories_slice = toshl_categories[offset:offset+page_size]
    for c in toshl_categories_slice:
      print(f"[{ind}] {c['name']}")
      ind += 1
    print("")
    print("[<] Prev page        [>] Next page")
    print(f"[b] Back to friend's expenses")

    while(True): # collect user input
      i = input()
      if i == ">":
        offset += page_size
        if offset > len(toshl_categories) - page_size:
          offset = max(0, len(toshl_categories) - page_size)
        break # Break out of input loop
      elif i == "<":
        offset -= page_size
        if offset < 0:
          offset = 0
        break # Break out of input loop
      elif i == 'b':
        bail = True
        break # Break out of input loop
      elif int(i) < 0 or int(i) >= len(toshl_categories_slice):
        print('Invalid input!')
        input("Press Enter to try again")
      else:
        selected_category = toshl_categories_slice[int(i)]
        finish = True
        break # Break out of input loop

    if bail or finish:
      break # Break out of category page loop
  return bail, selected_category

def get_tag(breadcrumb, expense, selected_category):
  offset = 0
  page_size = 15
  bail = False
  finish = False
  selected_tag = None
  while (True): # Paginate tags list
    clear()
    print(f"{breadcrumb} > Add Expense > Choose Tag") 
    print(f"==========================================") 
    print("")
    print("Adding expense:")
    print(splitwise_expense_long_string(expense))
    print("")
    print(f"Category: {selected_category['name']}")
    print(f"Choose your tag (showing {offset+1} to {offset+page_size+1})\n(You can only choose one, sorry. To add more use the app.s)")
    ind = 0
    selected_category_tags = selected_category['tags']
    category_tags_slice = selected_category_tags[offset:offset+page_size]
    print("[n] <no tag>")
    for t in category_tags_slice:
      print(f"[{ind}] {t['name']}")
      ind += 1
    print("")
    print("[<] Prev page        [>] Next page")
    print(f"[b] Back to friend's expenses")

    while(True): # Collect user input
      i = input()
      if i == ">":
        offset += page_size
        if offset > len(selected_category_tags) - page_size:
          offset = max(0, len(selected_category_tags) - page_size)
        break # Break out of input loop
      elif i == "<":
        offset -= page_size
        if offset < 0:
          offset = 0
        break # Break out of input loop
      elif i == 'n':
        finish = True
        break # Break out of input loop
      elif i == 'b':
        bail = True
        break # Break out of input loop
      elif int(i) < 0 or int(i) >= len(category_tags_slice):
        print('Invalid input!')
        input("Press Enter to try again")
      else:
        selected_tag = category_tags_slice[int(i)]
        finish = True
        break # Break out of input loop
    if bail or finish:
      break # Break out of category page loop
  return bail, selected_tag