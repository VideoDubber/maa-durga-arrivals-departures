import requests
from bs4 import BeautifulSoup
import json
from time import sleep

def scrape_navratri_rides(year):
    # URL for the target website with the input year
    url = f"https://www.drikpanchang.com/navratri/ashwin-shardiya-navratri-dates.html?year={year}"

    # Send an HTTP GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to load page with status code {response.status_code}")
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all divs with class 'dpContent' as there can be multiple
    dp_content_list = soup.find_all('div', class_='dpContent')

    # Initialize variables to store the arrival and departure words
    arrival_ride = None
    departure_ride = None

    # Loop through each dpContent element to find the relevant text
    for dp_content in dp_content_list:
        # Get the text content of the current dpContent element
        text_words = dp_content.get_text().split()

        # Loop through the words and look for "arrival on" and "departure on"
        for i, word in enumerate(text_words):
            if word.lower() == "arrival" and i+2 < len(text_words) and text_words[i+1].lower() == "on":
                arrival_ride = text_words[i+2]  # The next word after "arrival on"
            if word.lower() == "departure" and i+2 < len(text_words) and text_words[i+1].lower() == "on":
                departure_ride = text_words[i+2]  # The next word after "departure on"

        # If both arrival and departure rides are found, no need to continue
        if arrival_ride and departure_ride:
            break
    arrival_ride=arrival_ride.replace("Goddess","")
    # Return the arrival and departure rides as a tuple

    return arrival_ride, departure_ride

# Example usage
year = 2024
arrival, departure = scrape_navratri_rides(year)
rides_dict={}
for year in range(1000):
    try:
        arrival, departure = scrape_navratri_rides(2024-year)
        rides_dict[2024-year]=[arrival, departure]
        with open("./rides_data.json","w") as f:
            json.dump(rides_dict,f)

    except:
        print(year)
        sleep(1)
        pass;


