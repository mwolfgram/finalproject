import sqlite3
import requests
import json
from bs4 import BeautifulSoup
import plotly.plotly as py
import plotly.graph_objs as go
import random

def load_help_text():
    with open('help.txt') as f:
        return f.read()

def fetch_data_pls_1 ():
    print('fetching data from fetch_data_pls_1!!')

def process_command_1(param):
    print(prarm + 'pls work')

def interactive_prompt():
    #****************** add regeneration options to help.txt??
    #****************** add os.remove if cache already exists and the user wants to be extra and get everything all over again???
    help_text = load_help_text()
    #print(help_text)
    #init_db(DBNAME)
    #help_text = load_help_text()
    response = ''
    while response.lower() != 'exit':
        response = input('hi! enter a command, type help for a list of commands, or exit: ')

        if response.lower() == 'help':
            print(help_text)
            continue

        if response.lower() == 'exit':
            print('boi bye')
            break

        DB_NAME = 'mobile.db'
        try:
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()
        except Error as e:
            print(e)

        statement1 = "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'mobiledata';"
        table_exists = cur.execute(statement1).fetchall()[0][0]
        if table_exists == 1:
            user_input = input('the information you need is already here! would you like to regenerate it? type "yes" or "no": ')

            if user_input == 'yes':
                print('getting new data -- this will take 5 to 30 minutes')
                fetch_data_pls_1()

            if user_input == 'no':
                print('okay, we will keep using the existing database')

            if response.lower() == 'exit':
                print('boi bye')
                break

        else:
            print('the table you need does not exist -- it will be generated again! this will take 5 to 30 minutes')
            fetch_data_pls_1()

        if 'bar ' in response.lower(): #reinforce this to handle error

            print('fetching data, be patient..........')
            try:
                #fetch_data_pls() #how to do it if it already exists?
                process_command_1(response)
            except:
                print('your graph command was not processed correctly')

        if 'scatter ' in response.lower(): #reinforce this to handle error
            print('fetching data, be patient..........')
            try:
                #fetch_data_pls()
                process_command_1(response)
            except:
                print('your graph command was not processed correctly')

        if response.lower() == 'help':
            print(help_text)
            #continue

        if response.lower() == 'exit':
            print('bye!')
            break

interactive_prompt()
