# **AIRPLANE ACCIDENT EVALUATION**
#open the AviationData file and convert to a list

from csv import reader
OAD = open('AviationData.txt')
RAD = reader(OAD, delimiter = '|')
aviation_data = list(RAD)


#try a QUADRATIC TIME approach (loop inside a loop) to find LAX94LA336
#open the AviationData file and convert to a list ##create lax empty list
lax_code =[]
#loop through data, looking for a given value
for l in aviation_data:
    for i in l:
        i = i.strip()
        if i == 'LAX94LA336':
#when value found, append row to lax_code
           lax_code.append(l)
print(lax_code)

##downside to the above approach is time used by computer looping 
##through file one row at a time and checking every elment of the 
##row against the conditional clause

##I think a vectorized search in using Pandas would be faster
##It would use linear time

##PANDAS APPROACH to find LAX94LA336

import pandas as pd
df = pd.read_csv('AviationData.txt', delimiter = '|')
df = df.apply(lambda x: x.str.strip())
lax = df[df.eq("LAX94LA366").any(1)]
print(lax)


##DICTIONARY APPROACH to find LAX94LA336

#strip leading and trailing whitespace from all strings
for counterl, valuel in enumerate(aviation_data):
    for counteri, valuei in enumerate(valuel):
        valuei = valuei.strip()
        aviation_data[counterl][counteri] = valuei

aviation_dict_cols = [] #list to contain column names
aviation_dict = {} #dictionary of row values keyed to column names
aviation_dict_list = [] #list of dictionaries from aviation_dict

#populate column names
for x in aviation_data[0]: 
    aviation_dict_cols.append(x)

length = len(aviation_data[0])
# # populate aviation_dict dictionary,append result to list of dictionaries 
for i in range(1, len(aviation_data)):
    aviation_dict = {} #clear values at the beginning of the loop
    for j in range(0,length):
        data = aviation_data[i][j]
        column = aviation_dict_cols[j]
        aviation_dict[column] = data
    aviation_dict_list.append(aviation_dict)

# # find LAX94LA336 in column 'Accident Number' 
lax_dict = []
for value in aviation_dict_list:
    if value["Accident Number"] == "LAX94LA336":
        lax_dict.append(value)
print(lax_dict)  
#Less code required to look through a list.  No dictionary needed to be created.

#Analyze accidents by state, injuries by month and year

df.rename(columns = {'Event Id ': 'Event Id', ' Investigation Type ':'Investigation Type',
       ' Event Date ': 'Event Date', ' Location ':'Location', ' Country ': 'Country', 
       ' Airport Code ': 'Airport Code', ' Injury Severity ': 'Injury Severity',
       ' Total Fatal Injuries ': 'Total Fatal Injuries',' Accident Number ':'Accident Number',
       ' Total Serious Injuries ': 'Total Serious Injuries', ' Total Minor Injuries ': 'Total Minor Injuries'}, inplace = True)


df.drop(columns = [' Latitude ', ' Longitude ', ' Airport Name ',    
       ' Aircraft Damage ', ' Aircraft Category ', ' Registration Number ',
       ' Make ', ' Model ', ' Amateur Built ', ' Number of Engines ',
       ' Engine Type ', ' FAR Description ', ' Schedule ',
       ' Purpose of Flight ', ' Air Carrier ',' Weather Condition ', 
       ' Broad Phase of Flight ',' Report Status ', ' Publication Date ', ' '],
        inplace = True)

import numpy as np
#clean injury columns for conversion to int
df['Total Fatal Injuries'] = df['Total Fatal Injuries'].replace(r'^\s*$', 0, regex=True)
df['Total Serious Injuries'] = df['Total Serious Injuries'].replace(r'^\s*$', 0, regex=True)
df['Total Minor Injuries'] = df['Total Minor Injuries'].replace(r'^\s*$', 0, regex=True)
df['Event Date'] = df['Event Date'].replace(r'^\s*$', '00/00/0000', regex=True)


#convert injury columns from string to int
df['Total Fatal Injuries'] = df['Total Fatal Injuries'].astype('int')
df['Total Serious Injuries'] = df['Total Serious Injuries'].astype('int')
df['Total Minor Injuries'] = df['Total Minor Injuries'].astype('int')

#extract month and year from Event Date
dfmonth = df["Event Date"].str.extract(pat = '(^[0-9]{2})')
dfyear = df["Event Date"].str.extract(pat = '([0-9]{4}$)')
dflocation= df["Location"].str.extract(pat = '([A-Z]{2}$)')

#merge month, year, location series onto df
df = pd.merge(left = df, right = dfmonth.to_frame(), left_index = True, right_index = True)
df = pd.merge(left = df, right = dflocation.to_frame(), left_index = True, right_index = True)
df = pd.merge(left = df, right = dfyear.to_frame(), left_index = True, right_index = True)
df = df.rename(columns = {'Event Date_y': "Month", 'Location_y':"State", "Event Date": "Year"})
# #Print state with most accidents
state_accidents = df.groupby('State').size().sort_values(ascending = False)
print("Most accidents (state and #):", '\n', state_accidents.head(1))
# For the years in this dataframe (1948 - 2015), California is the state with the most airplane injuries

# #Pivot table for injuries by year
pv_injuries_yr = df.pivot_table(index = ["Year"], values = ["Total Fatal Injuries", "Total Serious Injuries"], aggfunc = np.sum)
pv_injuries_yr["All Injuries"] =pv_injuries_yr["Total Fatal Injuries"] + pv_injuries_yr["Total Serious Injuries"]
pv_inj_yrsort = pv_injuries_yr.sort_values(by= "All Injuries",ascending = False)
print(pv_inj_yrsort.head(3))
#For the years in this dataframe (1948 - 2015), 1996 is the year with the most airplane injuries


#Pivot table for injuries by month
pv_injuries_mo = df.pivot_table(index = ["Month"], values = ["Total Fatal Injuries", "Total Serious Injuries"], aggfunc = np.sum)
pv_injuries_mo["All Injuries"] =pv_injuries_mo["Total Fatal Injuries"] + pv_injuries_mo["Total Serious Injuries"]
pv_inj_mosort = pv_injuries_mo.sort_values(by= "All Injuries",ascending = False)
print(pv_inj_mosort.head(3))
#Most airplane injuries occur from July- Sept.

