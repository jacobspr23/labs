import requests

API_KEY = "hMAuPgLTg1dx6NaUoZ0CRp6my2VG0O0pqVUt3DXh"
API_URL = "https://api.nasa.gov/planetary/apod"

# Fetches APOD for today, since no date parameter is used
response = requests.get(f"{API_URL}?api_key={API_KEY}")

def fetch_apod(date=None):
    """
    Fetches the Astronomy Picture of the Day (APOD) from NASA's API.
    
    Parameters:
        date (str): Date in the format 'YYYY-MM-DD'. If None, fetches today's APOD.
    
    Returns:
        dict: JSON data from the APOD API response.
    """
    # URL with optional date parameter
    params = {'api_key': API_KEY}
    if date:
        params['date'] = date

    response = requests.get(API_URL, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return JSON data if request is successful
    else:
        raise Exception(f"Failed to fetch data: Status code {response.status_code}")