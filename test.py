import re
import requests
from bs4 import BeautifulSoup

def search_product(search_value):
    # Step 1: Trim and replace parts of the search URL
    search_value = search_value.strip()
    search_value = search_value.replace('http://', ' http://')
    search_value = search_value.replace('https://', ' https://')
    search_value = search_value.replace('https://dl.flipkart.com', ' http://dl.flipkart.com')

    # Step 2: Validate the search value length
    if len(search_value) == 0:
        print("Please search something!")
        return

    # Step 3: Remove trailing '=' from search value
    while len(search_value) > 1 and search_value[-1] == '=':
        search_value = search_value[:-1]

    # Step 4: Extract URLs from the search value using regex
    matches = re.findall(r'\bhttps?:\/\/\S+', search_value)
    if matches:
        # Step 5: Prepare data for POST request
        product_url = matches[0]
        print(f"Sending request for: {product_url}")
        
        # Step 6: Send the POST request to the API
        response = requests.post(
            "https://pricehistory.app/api/search",
            headers={'Content-Type': 'application/json'},
            json={'url': product_url}
        )

        # Step 7: Handle response
        if response.status_code == 200:
            data = response.json()
            if data.get('status'):
                # Redirect logic can be handled based on the response data
                redirect_url = f"https://pricehistory.app/p/{data['code']}"
                print(f"Redirecting to: {redirect_url}")
            else:
                print(f"Error: {data['message']}")
        else:
            print("Sorry, something went wrong!")
    else:
        # If no URLs are found, handle fallback search
        fallback_search_url = f"https://pricehistory.app/page/search#gsc.tab=0&gsc.q={search_value}"
        print(f"Redirecting to fallback search: {fallback_search_url}")


# Example usage
# Make the GET request

# Make the GET request to fetch the HTML content
url = 'https://amzn.in/d/5Xq6WEO'
resp = requests.get(url)



def search_product(search_value):
    # Step 1: Trim and replace parts of the search URL
    search_value = search_value.strip()
    search_value = search_value.replace('http://', ' http://')
    search_value = search_value.replace('https://', ' https://')
    search_value = search_value.replace('https://dl.flipkart.com', ' http://dl.flipkart.com')

    # Step 2: Validate the search value length
    if len(search_value) == 0:
        print("Please search something!")
        return

    # Step 3: Remove trailing '=' from search value
    while len(search_value) > 1 and search_value[-1] == '=':
        search_value = search_value[:-1]

    # Step 4: Extract URLs from the search value using regex
    matches = re.findall(r'\bhttps?:\/\/\S+', search_value)
    if matches:
        # Step 5: Prepare data for POST request
        product_url = matches[0]        
        # Step 6: Send the POST request to the API
        response = requests.post(
            "https://pricehistory.app/api/search",
            headers={'Content-Type': 'application/json'},
            json={'url': product_url}
        )

        # Step 7: Handle response
        if response.status_code == 200:
            data = response.json()
            if data.get('status'):
                # Redirect logic can be handled based on the response data
                redirect_url = f"https://pricehistory.app/p/{data['code']}"
                return redirect_url
            else:
                return f"Error: {data['message']}"
        else:
            return "Sorry, something went wrong!"
    else:
        # If no URLs are found, handle fallback search
        fallback_search_url = f"https://pricehistory.app/page/search#gsc.tab=0&gsc.q={search_value}"
        return fallback_search_url

print(search_product(url))