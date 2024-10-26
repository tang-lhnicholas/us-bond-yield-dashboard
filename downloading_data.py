import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import time

currentyear = datetime.now().year
lastyear = currentyear - 1
datetoday = datetime.today().strftime('%B-%d-%Y')
def downloaddata(startyear, endyear):
    data_list = []
    print('Downloading data. This should take less than a minute.')
    for year in range(startyear, endyear+1):
        url = f'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value={str(year)}'
        
        # Send a GET request to the URL
        start = time.time()
        response = requests.get(url)
        end = time.time()
        print(f'Request success. Time: {round(end - start, 3)}s')
        if response.status_code == 200:
            start=time.time()
            soup = BeautifulSoup(response.content, 'html.parser')
    
            # Find the table containing the data
            table = soup.find('table', class_='views-table')
    
            rows = table.find_all('tr')
    
            for row in rows[1:]:  # Skip the first row as it contains headers
                # Extract table data from each row
                data = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                data_dict = {
                    'Date': data[0],
                    '1 Mo': data[10],
                    '2 Mo': data[11],
                    '3 Mo': data[12],
                    '6 Mo': data[13],
                    '1 Yr': data[14],
                    '2 Yr': data[15],
                    '3 Yr': data[16],
                    '5 Yr': data[17],
                    '7 Yr': data[18],
                    '10 Yr': data[19],
                    '20 Yr': data[20],
                    '30 Yr': data[21]
                }
                data_list.append(data_dict)
            end = time.time()
            print(f'Parsing complete. Time: {round(end - start, 3)}s')
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data_list)
    return df


# Download data from 1990 to last year if data is not already local
if os.path.isfile(f'./Data/US Bond Yield Data from 1990-{lastyear}.csv') == True:
    pass

else:
    downloaddata(1990, lastyear).to_csv(f'Data/US Bond Yield Data from 1990-{lastyear}.csv', index=False)  

# Download data of most recent year if not done on the day

with open('Data/Last download date log.txt', 'r') as file:
    date = file.read()
    if date != str(datetoday) or os.path.isfile(f'./Data/US Bond Yield Data YTD {currentyear}.csv') == False:
        
        if os.path.isfile(f'./Data/US Bond Yield Data YTD {currentyear}.csv') == True: 
            os.remove(f'./Data/US Bond Yield Data YTD {currentyear}.csv')
            
        downloaddata(currentyear, currentyear).to_csv(f'Data/US Bond Yield Data YTD {currentyear}.csv', index=False)  
    
        # Merge the two files
        df1 = pd.read_csv(f'Data/US Bond Yield Data from 1990-{lastyear}.csv')
        df2 = pd.read_csv(f'Data/US Bond Yield Data YTD {currentyear}.csv')
        merged_df = pd.concat([df1, df2], ignore_index=True)
        
        if os.path.isfile(f'./Data/_US Bond Yield Data from 1990 to date.csv') == True: 
            os.remove(f'./Data/_US Bond Yield Data from 1990 to date.csv')
        merged_df.to_csv(f'Data/_US Bond Yield Data from 1990 to date.csv', index=False)
        open('Data/Last download date log.txt', 'w').write(str(datetoday))
        print(f'Data last updated: {datetoday}')
