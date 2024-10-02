import pandas as pd
import json
import numpy as np

# Load rainfall data from CSV
rainfall_df = pd.read_csv('rainfall.csv')
rainfall_df['YEAR']=rainfall_df['YEAR'].apply(lambda x:str(int(x)))
# Load rides data from JSON
with open('rides_data.json') as f:
    rides_data = json.load(f)

# Initialize a dictionary to store the annual rainfall from mid-Oct to mid-Oct
annual_rainfall = {}
years=set(rainfall_df['YEAR'])
# Iterate through each row in the rainfall DataFrame
for index, row in rainfall_df.iterrows():
    year = int(row['YEAR'])

    # Check if the previous year's data is available
    if str(year - 1) in years:
        
        # Extract rainfall data for the current year
        jan = row['JAN']
        feb = row['FEB']
        mar = row['MAR']
        apr = row['APR']
        may = row['MAY']
        jun = row['JUN']
        jul = row['JUL']
        aug = row['AUG']
        sep = row['SEP']
        
        # Extract rainfall data for the previous year
        prev_year = str(int(year) - 1)
        prev_row = rainfall_df[rainfall_df['YEAR'] == prev_year].iloc[0]
        oct_rain_prev = prev_row['OCT']
        nov_rain_prev = prev_row['NOV']
        dec_rain_prev = prev_row['DEC']
        
        # Calculate annual rainfall from mid-Oct to mid-Oct
        total_rainfall = (oct_rain_prev / 2) + nov_rain_prev + dec_rain_prev + jan + feb + mar + apr + may + jun + jul + aug + sep
        
        # Store the result in the annual_rainfall dictionary
        annual_rainfall[year] = total_rainfall

# Display the compiled annual rainfall data
for year, rainfall in annual_rainfall.items():
    print(f"Year: {year}, Annual Rainfall (mid-Oct to mid-Oct): {rainfall}")

#same year arrival rides, before which current year(Oct-Oct) ends
arrival_array=[rides_data[str(year)][0] for year in range(1902,2013)]
#prev year departure rides after which current year(Oct-Oct) starts
departure_array=[rides_data[str(year-1)][1] for year in range(1902,2013)]



def get_rainfall_arrival_ride(arrival_ride_="",f=np.mean):
    return([f([annual_rainfall[year] for year in range(1902,2013) if rides_data[str(year-1)][0]==arrival_ride_]),
    f([annual_rainfall[year] for year in range(1902,2013) if rides_data[str(year-1)][0]!=arrival_ride_])]
                    )
def get_rainfall_departure_ride(departure_ride_="",f=np.mean):
    return([f([annual_rainfall[year] for year in range(1902,2013) if rides_data[str(year-1)][1]==departure_ride_]),
    f([annual_rainfall[year] for year in range(1902,2013) if rides_data[str(year-1)][1]!=departure_ride_])]
                    )
from collections import Counter as c
print(c(arrival_array))
print(c(departure_array))
print(set(arrival_array))
print(set(departure_array))
print("Average rainfall in years for coming by Boat and not coming by Boat:",get_rainfall_arrival_ride("Boat"))

print("Average rainfall in years for coming by Elephant and not coming by Elephant:",get_rainfall_arrival_ride("Elephant"))

print("Average rainfall in years for departing on Elephant and not departing on Elephant:",get_rainfall_departure_ride("Elephant"))

print("Median rainfall in years for coming by Boat and not coming by Boat:",get_rainfall_arrival_ride("Boat",np.median))
print("Average rainfall in years for coming by Elephant and not coming by Elephant:",get_rainfall_arrival_ride("Elephant",np.median))


print("Median rainfall in years for departing on Elephant and not departing on Elephant:",get_rainfall_departure_ride("Elephant",np.median))








