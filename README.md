# Splitwise to Toshl
This is a command line application that will take your expenses in splitwise and automatically input them into toshl.

## Development
You need to have python 3 installed

## Usage

This also only runs on your personal accounts. You need to get the API keys from both these services and input them into your config file. There is an example config file provided.

Run this command after you have set up the config files.
```sh
python main.py
```

To use the program, key in the number or letter in the `[]` brackets and press Enter.

All other necessary instructions should be in the program itself.

This is roughly how the program works.

```
Main Menu
  - Add expenses from friends List
    - Choose a Friend
      - Choose a page of expenses
        - Add expense
          - Choose a category
          - Choose a tag
          - Expense added, go to next expense
  - Add expenses from groups list (not implemented)
    - Choose a Group
      - Choose a page of expenses
        - Add expense
          - Choose a category
          - Choose a tag
          - Expense added, go to next expense
  - Exit

```

## Future Improvements
- Add group support
- Refactor code so it's not all one huge file
- Preload all toshl expenses so we don't keep loading per expense
