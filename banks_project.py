from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime 

# Declaring known values for the ETL process
url = 'https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs_extract = ["Name", "MC_USD_Billion"]  # Columns to extract from the webpage table
table_attribs = ["MC_EUR_Billion", "MC_GBP_Billion", "MC_INR_Billion"]  # Columns for transformations
csv_path = './Largest_banks_data.csv'  # Path for saving the transformed CSV
db_name = 'Banks.db'  # Name of the SQLite database
table_name = 'Largest_banks'  # Name of the table in the SQLite database
rows_data = []  # Placeholder list to hold extracted row data

def log_progress(message):
    ''' 
    This function logs the mentioned message of a given stage of the 
    code execution to a log file. Function returns nothing.
    '''
    timestamp_format = '%Y-%h-%d-%H:%M:%S'  # Define the timestamp format
    now = datetime.now()  # Get the current timestamp
    timestamp = now.strftime(timestamp_format)  # Format the timestamp
    with open("./code_log.txt", "a") as f:  # Open the log file in append mode
        f.write(timestamp + ' : ' + message + '\n')  # Write the message to the log

def extract(url):
    ''' 
    This function aims to extract the required information from the 
    website and save it to a DataFrame. Returns the DataFrame for 
    further processing.
    '''
    url_text = requests.get(url).text  # Fetch the webpage content
    html_soup = BeautifulSoup(url_text, 'html.parser')  # Parse the webpage content using BeautifulSoup
    elements = html_soup.find_all('tbody')  # Locate the <tbody> elements in the HTML
    rows = elements[0].find_all('tr')  # Extract all rows (<tr>) within the first <tbody>

    for row in rows:
        cells = row.find_all('td')  # Extract all cells (<td>) within the row
        if len(cells) == 3:  # Ensure the row has exactly three cells
            second_column = cells[1].text.strip()  # Extract and clean the second cell
            third_column = cells[2].text.strip()  # Extract and clean the third cell
            data_dict = {
                "Name": second_column,  # Add the second cell as 'Name'
                "MC_USD_Billion": float(third_column)  # Add the third cell as 'MC_USD_Billion' and convert to float
            }
            rows_data.append(data_dict)  # Append the dictionary to the list
    df = pd.DataFrame(rows_data)  # Convert the list of dictionaries to a DataFrame
    return df

def transform(df):
    ''' 
    This function accesses the CSV file for exchange rate information, 
    and adds three columns to the DataFrame, each containing the 
    transformed version of the Market Cap column in respective currencies.
    '''
    dataframe = pd.read_csv('exchange_rate.csv')  # Load the CSV file with exchange rates
    csv_dict = dataframe.set_index('Currency').to_dict()['Rate']  # Convert the exchange rates to a dictionary

    for i, column in enumerate(csv_dict):  
        if column not in df.columns:  # If the column does not already exist
            rate = list(csv_dict.values())[i]  # Fetch the exchange rate
            df[table_attribs[i]] = [np.round(val * rate, 2) for val in df['MC_USD_Billion']]  # Apply the exchange rate
    return df

def load_to_csv(df, csv_path):
    ''' 
    This function saves the final DataFrame as a CSV file in 
    the provided path. Function returns nothing.
    '''
    df.to_csv(csv_path)  # Save the DataFrame to a CSV file

def load_to_db(df, sql_connection, table_name):
    ''' 
    This function saves the final DataFrame to a database 
    table with the provided name. Function returns nothing.
    '''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)  # Save the DataFrame to the database

def run_query(query_statement, sql_connection):
    ''' 
    This function runs the query on the database table and 
    prints the output on the terminal. Function returns nothing.
    '''
    print(f"Executing Query: {query_statement}")  # Log the query being executed
    query_output = pd.read_sql(query_statement, sql_connection)  # Execute the query and fetch results
    print(query_output)  # Print the query results
    print('\n\n\n') 
    return query_output  

# Execution of the ETL pipeline

log_progress("Preliminaries complete. Initiating ETL process.")  # Log the start of the process

# Step 1: Data extraction
df = extract(url)  # Extract data from the URL
log_progress("Data extraction complete. Initiating Transformation process.")  # Log extraction completion

# Step 2: Data transformation
df = transform(df)  # Transform the extracted data
log_progress("Data transformation complete. Initiating Loading process.")  # Log transformation completion

# Step 3: Load data to CSV
load_to_csv(df, csv_path)  # Save the transformed data to a CSV file
log_progress("Data saved to CSV file.")  # Log CSV save completion

# Step 4: Load data to SQLite database
sql_connection = sqlite3.connect(db_name)  # Initiate a connection to the SQLite database
log_progress("SQL Connection initiated.")  # Log connection initiation
load_to_db(df, sql_connection, table_name)  # Save data to the database
log_progress("Data loaded to Database as a table, Executing queries.")  # Log database load completion

# Step 5: Run queries on the database
run_query("SELECT * FROM Largest_banks", sql_connection)  # Query 1: Display all data
run_query("SELECT AVG(MC_GBP_Billion) AS Avg_Market_Cap_GBP FROM Largest_banks", sql_connection)  # Query 2: Average Market Cap
run_query("SELECT Name FROM Largest_banks LIMIT 5", sql_connection)  # Query 3: Top 5 banks

log_progress("Process Complete.")  # Log query execution completion

# Step 6: Close the database connection
sql_connection.close()  # Close the SQLite database connection
log_progress("Server Connection closed.")  # Log server connection closure
