from KrogerTokenManager import KrogerTokenManager

# Configuration
CLIENT_ID = "testv1-bbc7twz6"
CLIENT_SECRET = "BPmNqMzGmxMRs4EHPqciaeoeZAok6a54KrLYv9aO"
SCOPE = "product.compact"
AUTH_URL = "https://api-ce.kroger.com/v1/connect/oauth2/token"

# Token Manager
token_manager = KrogerTokenManager(CLIENT_ID, CLIENT_SECRET, SCOPE, AUTH_URL)

# Make Product API Call
brand = "Kroger"
term = "milk"
location_id = "03500577"

token_manager.get_product_details(brand, term, location_id)