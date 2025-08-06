##create class that refreshes token
import json
import time

import requests


class KrogerTokenManager:
    def __init__(self, client_id, client_secret, scope, auth_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.auth_url = auth_url
        self.token = None
        self.token_expiry = 0  # Epoch timestamp

    def _encode_credentials(self):
        import base64
        credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(credentials.encode()).decode()

    def get_token(self):
        # If current time is before token_expiry, return cached token
        if self.token and (time.time() < self.token_expiry):
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

    def get_locations(self, zip_code, num_of_location):
        url = f"https://api-ce.kroger.com/v1/locations?filter.zipCode.near={zip_code}&filter.limit={num_of_location}"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.get_token()}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            # Write to a JSON file
            with open('outputs\\locations.json', 'w') as f:
                json.dump(data, f, indent=4)

        else:
            print(f"Request failed with status code {response.status_code}")

    def get_product_details(self, brand, term, location_id):
        url = f"https://api-ce.kroger.com/v1/products?filter.brand={brand}&filter.term={term}&filter.locationId={location_id}"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.get_token()}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            # Write to a JSON file
            with open(f'outputs\\{brand}_{term}_{location_id}_details.json', 'w') as f:
                json.dump(data, f, indent=4)
        else:
            print(f"Request failed with status code {response.status_code}")