# %% [markdown]
# The purpose of this file is for collection of data from the user, we put the functions related to this in this file

# %% [markdown]
# So, we would firstly import needed classes, modules etc

# %%
from datetime import datetime


# %% [markdown]
# Writing the functions

# %%
#We get the date

date_format = '%d-%m-%Y' #Put this back up here so we can use just date format instead of retyping '%d-%m-%Y'
CATEGORIES = {'I': 'Income', 'E': 'Expense'}

def get_date(prompt, allow_default = False):
    date_str = input(prompt) 
    if allow_default and not date_str:
        return datetime.today().strftime(date_format) 
    
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print('invalid date format. Please enter the date in dd-mm-yyyy format')
        return get_date(prompt, allow_default)

#We get the amount
def get_amount():
    try:
        amount = float(input('Enter the amount: '))
        if amount <= 0:
            raise ValueError('Amount must be a non-negative non-zero value.')
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


#We get the category
def get_category():
    category = input("Enter the category('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:  
        return CATEGORIES[category]
    
    print("Invalid category. Please enter 'I' for income or 'E' for expense")
    return get_category()

#We get the description
def get_description():
    return input("Enter a description (optional): ")





