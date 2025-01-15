"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Simona Kurucová
email: kurucovas11@protonmail.com
"""

import requests
from bs4 import BeautifulSoup as bs
import argparse
import csv
import re
import pandas as pd

def main():
    # Call parse function to get URL and file name
    vybrana_url, vystupny_subor = parse()

    # Call scrape function to get code and location:
    číslo, název = scrape_code_location(vybrana_url)

    print(f"STAHUJI DATA Z VYBRANÉHO URL:{vybrana_url}")

    #Initialize lists for next data:
    volici = []
    obalky = []
    platne_hlasy = []
    party_names, vote_counts = [], []

    # Get data from the next URL page for each "číslo" in the list
    for číslo_value in číslo:
        next_page_url = get_next_page_url(vybrana_url, číslo_value)
        # scrape the values from the next page
        volici_value, obalky_value, platne_hlasy_value = scrape_and_save_values(next_page_url, číslo_value, vystupny_subor)
        volici.append(volici_value)
        obalky.append(obalky_value)
        platne_hlasy.append(platne_hlasy_value)
        # scrape the party names and vote counts from the next page
        parties, votes = scrape_parties_and_votes(next_page_url)
        party_names.append(parties)
        vote_counts.append(votes)

    print(f"UKLADÁM DO SÚBORU: {vystupny_subor}")

    # Save all values to CSV
    save_to_csv(číslo, název, volici, obalky, platne_hlasy, party_names, vote_counts, vystupny_subor)
 
    #load_csv_to_table(vystupny_subor)                          # After saving the CSV, load it and print the table

    print("UKONČUJI election-scraper")  

def parse():
    # Set up argument parser:
    parser = argparse.ArgumentParser(description="Scrape election results for selected territorial unit and save to csv file.")
    # Define 2 obligatory arguments:
    parser.add_argument('territorial_unit_url', type=valid_url, help="URL of territorial unit's election results (e.g., https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103)")
    parser.add_argument('file_name', type=str, help="Name of output csv file (e.g., results_prostejov.csv)")
    # Parse the arguments
    args = parser.parse_args()
    vybrana_url = args.territorial_unit_url
    vystupny_subor = args.file_name
    return vybrana_url, vystupny_subor

def valid_url(url):
    # Correct the pattern for matching the URL structure
    pattern = r"^https:\/\/www\.volby\.cz\/pls\/ps2017nss\/ps32\?xjazyk=CZ&xkraj=\d{1,2}&xnumnuts=\d{4}$"
    if re.match(pattern, url):
        return url
    else:
        raise argparse.ArgumentTypeError("Invalid URL address or incorrect order of arguments.")

def scrape_code_location(vybrana_url):  
    response = requests.get(vybrana_url)                      # Send GET request to provided URL
    soup = bs(response.content, 'html.parser')                # Parse the content with library BeautifulSoup
    # Find all tables and rows in the HTML
    tables = soup.find_all('table')
    rows = soup.find_all('tr')                                # Extract data from rows in table (tr = table row)
    # Lists to hold the "číslo" and "název" values
    číslo = []
    název = []
    # Loop through each row found in the HTML table
    for row in rows:
        columns = row.find_all('td')                          # Find all td (table cells) in a row
        if len(columns) < 2:
            continue                                          # Skip rows that don't have at least 2 columns   
        číslo_value = columns[0].text.strip()                 # Extract data from 1st column
        název_value = columns[1].text.strip()                 # Extract data from 2nd column
        # Append extracted data to the lists
        číslo.append(číslo_value)
        název.append(název_value)
    return číslo, název                                       # Return lists containing extracted values

def get_next_page_url(vybrana_url, číslo):
    match = re.search(r'xjazyk=([A-Za-z]+)&xkraj=(\d{1,2})&xnumnuts=(\d{4})', vybrana_url)
    if match:
        xjazyk = match.group(1)
        xkraj = match.group(2)
        xnumnuts = match.group(3)
    else:
        print("Invalid URL format.")
        return None
    # Construct next page URL 
    next_page_url = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk={xjazyk}&xkraj={xkraj}&xobec={číslo}&xvyber={xnumnuts}"
    return next_page_url

def scrape_and_save_values(next_page_url, číslo_value, vystupny_subor):
    response = requests.get(next_page_url)                         # Send GET request to the next page URL
    soup = bs(response.content, 'html.parser')
    table = soup.find('table')                                     # Find table containing data
    # Lists to store next data:
    volici_value = []
    obalky_value = []
    platne_hlasy_value = []
    
    if table:
        columns = table.find_all('td')
        if len(columns) >= 8:                                     
            volici_value = columns[3].text.strip()  
            obalky_value = columns[4].text.strip()  
            platne_hlasy_value = columns[7].text.strip()  
            return volici_value, obalky_value, platne_hlasy_value
    return volici_value, obalky_value, platne_hlasy_value         # Return empty values if not found asked table

def scrape_parties_and_votes(next_page_url):
    response = requests.get(next_page_url)                        # Send GET request to next page URL
    soup = bs(response.content, 'html.parser')
    tables = soup.find_all('table')                               
    parties = []                                                  # Initialize list to store the party names 
    votes = []                                                    # Initialize list to store votes
    if len(tables) >= 3:                                          # Check if there are at least 3 tables on the page 
        table_2 = tables[1]                                       # Scraping party names and votes from table 2
        rows_2 = table_2.find_all('tr')
        for row in rows_2:
            columns = row.find_all('td')
            if len(columns) >= 3:                                 # Checking if the row has enough columns
                party_name = columns[1].text.strip()  
                vote_count = columns[2].text.strip()  
                parties.append(party_name)
                votes.append(vote_count)

        table_3 = tables[2]                                       # Scraping party names and votes from table 3
        rows_3 = table_3.find_all('tr')
        for row in rows_3:
            columns = row.find_all('td')
            if len(columns) >= 3:                                 # Checking if the row has enough columns
                party_name = columns[1].text.strip()  
                vote_count = columns[2].text.strip()  
                parties.append(party_name)
                votes.append(vote_count)
    return parties, votes

def save_to_csv(číslo, název, volici=None, obalky=None, platne_hlasy=None, party_names=None, vote_counts=None, vystupny_subor=None):
    # Open csv file for writing (or appending if it already exists)
    with open(vystupny_subor, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:                                               # if it's 1. writing (empty file), write header row
            header = ["číslo", "název", "voliči v seznamu", "vydané obálky", "platné hlasy"] 
            if party_names:                                                # if party names are provided, append them to header
                for party in party_names[0]:                               # only include unique party names
                    header.append(party) 
            writer.writerow(header)
        # Write each row of data
        for c, n, v, o, p, parties, votes in zip(číslo, název, volici or [], obalky or [], platne_hlasy or [], party_names or [], vote_counts or []):
            row = [c, n, v, o, p]                                                # prepare row with general election data
            if parties and votes:                                                
                row += votes                                                     # add vote counts for each party
            # Remove any empty lists, strings, or commas before any other modifications
            row = [value for value in row if value not in ('', [], ',')]
            # Strip `-` from each value in the row 
            row = [str(value).rstrip('-') for value in row]
            # Skip the row if it contains only empty values
            if not row or all(value == '' for value in row):  
                continue                             
            if row and row[-1] == '':
                row.pop()                                                         # remove "," if it's the last element
            writer.writerow(row)
            #print(f"{c}, {n}, {v}, {o}, {p}, {', '.join(votes) if votes else ''}")

def load_csv_to_table(vystupny_subor):                                           # Function to load csv into a pandas DataFrame and display table
    df = pd.read_csv(vystupny_subor)                                             # Read csv file into a pandas DataFrame
    print(df)                                                                    # Display table (DataFrame)

# Run the script
if __name__ == "__main__":
    main()