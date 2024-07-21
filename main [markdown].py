# %% [markdown]
# 1) Installation and importation of needed modules. They include matplotlib(this would help with plotting needed graphs) and Pandas(pandas would help us easily categorize and search for data within our csv file). I already have these installed, so I would just be importing them. However, to install from within IDE in Jupyter notebook, you can use !module name or %module name

# %%
%pip install pandas 
%pip install matplotlib
import pandas as pd 
import csv
import matplotlib.pyplot as plt
from datetime import datetime
#%pip install nbimporter #I installed this Jupyter noteboook extension to allow for me to import code from Jupyter notebooks, then now importing the files in data_entry.ipynb by importing the I will describe as callings of the functions we created in data_entry
#import nbimporter #to enable me import data_entry directly in Jupyter notebook without converting the document to .py
from data_entrypy import get_amount, get_category, get_date, get_description


# %% [markdown]
# 2. I will set up a class that would allow for ease of working with the csv file

# %%
class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['date', 'amount', 'category', 'description']
    FORMAT = '%d-%m-%Y'

    #We need to then initialise the csv file(ie read it in or create it,hence, creation of the init method below)
    @classmethod #The def initialize_csv is a class method, hence the @classmethod here just before the initialize_csv method
    def initialize_csv(cls):
        try: #here we are then trying to read in the csv file below
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns = cls.COLUMNS) #b()
            #Below I will be exporting the dataframe to a csv file
            df.to_csv(cls.CSV_FILE, index=False)

    #The csv file below indicated by #a has been confirmed to exist, as we ran it, so now we want to add some entries to the file.
    # we will add a method now to the class as below
    @classmethod
    def add_entry(cls, date, amount, category, description): #then we add the entries as have been done on this line(pls keep in mind that the category can vary, these are just the ones I added in this project, also it should align with the category names after inputing "cls,")
        #We then use a csv writer, Pandas can as well help, to write into the file
        #So we create the entry we will be adding as like below
        new_entry = {
            'date': date,
            'amount': amount,
            'category': category,
            'description': description
        }
        #So we specified all of the columns associated with their values. We stored this in a Python dictionary as we can use the Python dictionary to write into the correct columns when we use the csv writer
        #Here it goes
        with open(cls.CSV_FILE, 'a', newline = '') as csvfile: #Here we open the csv file in append mode, that is the reason for the 'a' there
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS) #So here, a csv writer was created taking a dictionary and writing it into a csv file
            #Now that we have created this object, we can use it
            writer.writerow(new_entry)
        print('Entry added successfully')

    @classmethod
    #we want to create a function to give us all the transactions within a date range
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        #we would be converting all of the dates inside the date column to a datetime object so that we can use them to get the filter by transactions
        df['date'] = pd.to_datetime(df['date'], format = CSV.FORMAT)    
        start_date = datetime.strptime(start_date,CSV.FORMAT)
        end_date = datetime.strptime(end_date,CSV.FORMAT)
        #We would be creating a mask at this point to guide on date selection
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df.loc[mask] #This would return a new filtered dataframe that only contains the rows where mask just above was True

        if filtered_df.empty:
            print('No transactions found in the given date range.')
        else:
            print(
                f'Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}'
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={'date': lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df['category'] == 'Income']['amount'].sum()
            total_expense = filtered_df[filtered_df['category'] == 'Expense']['amount'].sum()
            print('\nSummary')
            print(f'Total Income: ${total_income:.2f}')
            print(f'Total Expense: ${total_expense:.2f}')
            print(f'Net Savings: ${(total_income-total_expense):.2f}')

        return filtered_df


#We will be writing a function here that will call the functions we created in data_entry in the order we want in order to collect our data
def add():
    CSV.initialize_csv() #here we initialized the csv file
    #then we will get the values
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)



#To get the transactions summary(total income, total expense and Net savings)
#CSV.get_transactions('01-01-2023', '30-07-2024')


#This is for the graph
def plot_transactions(df):
    df.set_index('date', inplace=True)
#We set up the income dataframe(that is like the income aspect of a statistical table that will be used to create the graph)
    income_df = (
        df[df['category'] == 'Income']
        .resample('D')
        .sum()
        .reindex(df.index, fill_value=0)
    ) #resample fills in all the missing days, accounts for missing values grouping the data into regular time intervals and then applies an aggregation function(like mean, sum, etc) to each group. The ‘D’ in resample('D') stands for ‘Day’. It means the data will be resampled over daily intervals. If there are multiple entries in a single day, they will be aggregated (by default, the mean is calculated) to give one value per day. If there are missing days, they will appear as NaN in the resampled data unless you fill them using methods like ffill(), bfill(), or interpolate().
    #fill_value=0 is what fills in missing values with 0

     #We set up the expense dataframe
    expense_df = (
        df[df['category'] == 'Expense']
        .resample('D')
        .sum()
        .reindex(df.index, fill_value=0)
    )

#We would now be creating a plot using Matplotlib
    plt.figure(figsize=(10, 5)) #Providing dimensions for the plot/graph
    plt.plot(income_df.index, income_df['amount'], label='Income', color='g') #income
    plt.plot(expense_df.index, expense_df['amount'], label='Expense', color='r') #expense 
    plt.xlabel('Date') #the x-coordinate
    plt.ylabel('amount') #the y-coordinate
    plt.title('Income and expenses over time') #adding the title for the graph
    plt.legend() #enables the legends(we will see the labels for the colored lines)
    plt.grid(True) #This enables the grid lines
    plt.show() #This is what actually takes the plot and shows it on screen



#To make the finance tracker a bit more interactive, like it asking us what do you want to do, do you want to add money and such
def main():
    while True:
        print('\n1. Add new transaction')
        print('2.View transactions and a summary within a date range')
        print('3. Exit')
        choice = input('Enter your choice (1-3): ')

        if choice == '1':
            add()
        elif choice == '2':
            start_date = get_date('Enter the start date(dd-mm-yyyy)')
            end_date = get_date('Enter the end date(dd-mm-yyyy)')
            df = CSV.get_transactions(start_date, end_date)
            if input('Do you want to see a plot? (y/n)').lower() == 'y':
                plot_transactions(df)
        elif choice == '3':
            print('Exiting...')
            break
        else:
            print('Invalid choice. Enter 1,2 or 3.')

#This next line is protective so that it is when this file is executed that this runs and not an execution of or from another file
if __name__ =='__main__':
    main()


#We can test these by calling the add function
add()



#I will be testing the above below by running the method, if in Jupyter notebook as I am using, run the cells above as well, or if no code cells below this cell, run all cells for the file to be created
# CSV.initialize_csv() #a
# CSV.add_entry('20-07-2024', 125.65, 'Income', 'salary')










