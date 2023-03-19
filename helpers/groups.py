import requests
import json

from .common import *
from .expense import *

def group_transfer_page():
    clear()
    print(f"Friend Transfer ")
    print(f"==========================================")
    print("")
    print("Loading friends list:")
    r = requests.get(
        'https://secure.splitwise.com/api/v3.0/get_groups', headers=splitwise_headers)
    groups_arr = json.loads(r.text)['groups']
    print("Which groups's expenses do you want to sync?")
    friends_with_balances = []
    ind = 0
    user_id = user_accounts['splitwise']['id']
    for g in groups_arr:
        if (g['name'] != 'Non-group expenses'):
            for g_debts in g['original_debts']:
                if (g_debts['from'] == user_id or g_debts['to'] == user_id):
                    print(f"[{str(ind)}] {g['name']}")
                    friends_with_balances.append(g)
                    ind = ind + 1
                    break

    selected_friend = None
    while (True):
        i = input()
        if (int(i) < 0 or int(i) >= len(friends_with_balances)):
            print('Invalid input!')
            input("Press Enter to try again")
        else:
            selected_friend = friends_with_balances[int(i)]
            break

    page = 1
    group_expenses_page_list(selected_friend, page)


def group_expenses_page_list(selected_friend, page):
    while (True):  # User input
        clear()
        full_name = selected_friend['name']
        print(f"Group Transfer > {full_name} > Page {page}")
        print(f"==========================================")
        print("")
        print("Loading expenses for " + full_name + "\n")

        expenses = get_group_expenses(selected_friend["id"], 10, page - 1)

        # Give users some UI to decide what expenses they want.
        if len(expenses) == 0:
            print("There were no expenses here, you can try loading the next page")
        else:
            print("Here is what we found:")
            for e in expenses:
                print("   " + splitwise_expense_short_string(e))

        print("")
        print("Choose an option")
        print("[1] Start processing (you can skip individual expenses)")
        print("[2] Next page")
        print("[3] Prev page")
        print("[0] Back to main menu")

        i = input()
        if (i == '1'):
            process_group_expenses(expenses, full_name, page)
            page += 1
            continue
        elif (i == '2'):
            page += 1
            continue
        elif (i == '3'):
            page -= 1
            if page < 0:
                page = 0
            continue
        elif (i == '0'):
            break
        else:
            print('Invalid input!')
            input("Press Enter to go to next expense")


def process_group_expenses(expenses, full_name, page):
    expense_ind = 1
    for e in expenses:
        clear()
        print(
            f"Friend Transfer > {full_name} > Page {page} > Item {expense_ind} of {len(expenses)}")
        print(f"==========================================")
        print("")
        print(splitwise_expense_long_string(e))
        print("")

        dates = get_date_buffer(e['date'])
        print(
            f"Checking for similar expenses on Toshl from {dates[0]} to {dates[1]}")
        # Check toshl for similar expenses
        r = requests.get(
            f"https://api.toshl.com/entries?type=expense&from={dates[0]}&to={dates[1]}", headers=toshl_headers)
        toshl_entries = json.loads(r.text)
        similar_entries = get_similar_toshl_entries(e, toshl_entries)
        if len(similar_entries) == 0:
            print("   No similar expenses found")
        else:
            print(f"   Found {len(similar_entries)} similar expenses:")
            for se in similar_entries:
                print(f'    - {toshl_entry_short_string(se)}')

        print("")
        # Give options to add, or skip
        print("Choose an option")
        print("[1] Add expense (you need to provide the category and tags)")
        print("[2] Next expense")
        print("[0] Finish this page and go back")

        i = input()
        if (i == '1'):
            breadcrumb = f"Friend Transfer > {full_name} > Page {page} > Item {expense_ind} of {len(expenses)}"
            bail = add_expense(breadcrumb, e)
            if bail:
                break
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


def get_group_expenses(group_id, count, page):
    r = requests.get(
        f'https://secure.splitwise.com/api/v3.0/get_expenses?group_id={group_id}&limit={count}&offset={page * count}', headers=splitwise_headers)
    involved_expenses_arr = []
    expenses_arr = json.loads(r.text)['expenses']
    for e in expenses_arr:
        expense = {
            "category": e['category']['name'],
            "description": e['description'],
            "currency": e['currency_code'],
            "total_amount": float(e['cost']),
            "date": e['date'].split('T')[0],
            "share_amount": 0,
            "friends": []
        }

        expense_users = e['users']
        for eu in expense_users:
            if (eu['user']['id'] != user_accounts["splitwise"]["id"]):
                full_name = ' '.join(
                    filter(None, (eu['user']['first_name'], eu['user']['last_name'])))
                expense['friends'].append(full_name)
        for eu in expense_users:
            if eu['user_id'] == user_accounts['splitwise']['id']:
                expense['share_amount'] = float(eu['owed_share'])
                break

        if expense['share_amount'] > 0:
            involved_expenses_arr.append(expense)
            # pp.pprint(expense)
    return involved_expenses_arr
