# Importing necessary libraries.
import requests
import pandas as pd
import csv
from requests.exceptions import HTTPError
from pyusps import address_information


for url in ['https://tools.usps.com/zip-code-lookup.htm?byaddress', 'https://api.usps.com/invalid']:
    try:
        response = requests.get(url,allow_redirects=False)

        # If the response was successful, no Exception will be raised.
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  
    except Exception as err:
        print(f'Other error occurred: {err}') 
    else:
        print('Success!')

# Trying to validate the API.
url = "http://production.shippingapis.com/ShippingApi.dll?API=Verify&XML=<AddressValidateRequest USERID=\"141NIBS01737\"><Revision>1</Revision><Address ID=\"0\"><Address1></Address1><Address2>29851 Aventura k</Address2><City></City><State>CA</State><Zip5>92688</Zip5><Zip4></Zip4></Address></AddressValidateRequest>"

payload={}
files={}
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

# Printing the response inside the console.
print(response.text)

df = pd.read_csv("Python Quiz Input - Sheet1.csv")
  
# Initializing the titles as lists.
Company = []
Street = []
City = []
St = []
ZIPCode = []
   
# Reading csv file
with open("Python Quiz Input - Sheet1.csv", 'r') as csvfile:
    
    # Creating a csv reader object
    csvreader = csv.reader(csvfile)  
    # Extracting field names through first row
    fields = next(csvreader)
  
    # Appending each data to the row one by one
    for row in csvreader:
        Company.append(row[0])
        Street.append(row[1])
        City.append(row[2])
        St.append(row[3])
        ZIPCode.append(row[4])

# Creating an empty list to check whether the address is valid or invalid.
IsValid = []

# Checking for each record.
for i in range(0,len(Company)):
    # Appending "Valid" if the address is matched else appending "Invalid".
    try:
        addr = dict([
             ('address', Street[i]),
             ('city', City[i]),
             ('state', St[i]),
            ('zip5', ZIPCode[i]),
             ])
        
        print(address_information.verify('141NIBS01737', addr))
        IsValid.append("Valid")
    except Exception as e:
        IsValid.append("Invalid")
        print("Exception found", e)

# Checking whether the length matches the length of the original records.
print(len(IsValid) == len(Company))

# Adding a new column to the dataframe.
df["IsValid"] =  IsValid

# Permanently saving the file displaying an additional IsValid column.
df.to_csv("Python Quiz Input - Sheet1.csv")