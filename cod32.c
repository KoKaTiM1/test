import requests

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
url = "https://jsonplaceholder.typicode.com/todos/1"
data = fetch_data(url)

if data:
    print("Fetched data:")
    print(data)
else:
    print("Failed to fetch data")
d