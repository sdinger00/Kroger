import base64
import requests

pair = "testv1-bbc7twz6:BPmNqMzGmxMRs4EHPqciaeoeZAok6a54KrLYv9aO"
encoded = base64.b64encode(pair.encode('ascii')).decode('ascii')
authorization_header = f"Authorization: Basic {encoded}"

print(authorization_header)



url = "https://api-ce.kroger.com/v1/connect/oauth2/token"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Basic dGVzdHYxLWJiYzd0d3o2OkJQbU5xTXpHbXhNUnM0RUhQcWNpYWVvZVpBb2s2YTU0S3JMWXY5YU8="
}

body = {
    "grant_type": "client_credentials",
    "scope": "product.compact"
}

response = requests.post(url, headers=headers, data=body)

print(response.status_code)
response_data = response.json()
print(response_data)

access_token = response_data.get("access_token")
print("Access Token:", access_token)


brand = "Kroger"
term = "milk"
location_id = "01400943"

url = f"https://api-ce.kroger.com/v1/products?filter.brand={brand}&filter.term={term}&filter.locationId={location_id}"
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.json())