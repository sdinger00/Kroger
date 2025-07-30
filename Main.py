import base64
import requests
import time

##encode client id and secret
pair = "testv1-bbc7twz6:BPmNqMzGmxMRs4EHPqciaeoeZAok6a54KrLYv9aO"
encoded = base64.b64encode(pair.encode('ascii')).decode('ascii')
authorization_header = f"Authorization: Basic {encoded}"

print(authorization_header)

##get access token

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

##create class that refreshes token

class KrogerTokenManager:
    def __init__(self, client_id, client_secret, scope, auth_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.auth_url = auth_url
        self.token = None
        self.token_expiry = 0  # Epoch timestamp

    def get_token(self):
        # If current time is before token_expiry, return cached token
        if self.token and time.time() < self.token_expiry:
            return self.token

        # Otherwise, request new token
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {self._encode_credentials()}"
        }

        body = {
            "grant_type": "client_credentials",
            "scope": self.scope
        }

        response = requests.post(self.auth_url, headers=headers, data=body)
        response.raise_for_status()  # Raise an error if request failed

        data = response.json()
        self.token = data["access_token"]
        self.token_expiry = time.time() + data["expires_in"] - 60  # refresh 1 min before actual expiry

        return self.token

    def _encode_credentials(self):
        import base64
        credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(credentials.encode()).decode()

# Configuration
CLIENT_ID = "testv1-bbc7twz6"
CLIENT_SECRET = "BPmNqMzGmxMRs4EHPqciaeoeZAok6a54KrLYv9aO"
SCOPE = "product.compact"
AUTH_URL = "https://api-ce.kroger.com/v1/connect/oauth2/token"

# Token Manager
token_manager = KrogerTokenManager(CLIENT_ID, CLIENT_SECRET, SCOPE, AUTH_URL)

# Fetch Token When Needed
access_token = token_manager.get_token()


# Make Product API Call
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