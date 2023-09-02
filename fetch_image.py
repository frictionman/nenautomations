
# Developed by Nen AI

import requests

# Function to fetch photo from Pexels
def fetch_photo(query):
    # Placeholder for your Pexels API key
    api_key = 'YOUR_API_KEY'
    
    # Endpoint and headers for Pexels API
    url = 'https://api.pexels.com/v1/search'
    headers = {
        'Authorization': api_key,
    }
    params = {
        'query': query,
        'per_page': 1,
    }
    
    # Make the API request
    response = requests.get(url, headers=headers, params=params)
    
    # If successful, return the photo URL
    if response.status_code == 200:
        data = response.json()
        photos = data.get('photos', [])
        if photos:
            return photos[0]['src']['original']
    return None
