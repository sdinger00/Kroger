from KrogerTokenManager import KrogerTokenManager

# Configuration
CLIENT_ID = "testv1-bbc7twz6"
CLIENT_SECRET = "BPmNqMzGmxMRs4EHPqciaeoeZAok6a54KrLYv9aO"
SCOPE = "product.compact"
AUTH_URL = "https://api-ce.kroger.com/v1/connect/oauth2/token"

# Token Manager
kroger = KrogerTokenManager(CLIENT_ID, CLIENT_SECRET, SCOPE, AUTH_URL)

items = ["Flour", "Sugar", "Baking powder", "Salt", "Milk", "Egg", "Butter", "Vanilla extract"]
zip_code = 75039

closest_location_details = kroger.get_closest_location(zip_code)
closest_location_id = closest_location_details["locationId"]

# find the items in the store catalogue
item_details = []
for item in items:
    details = kroger.get_product_details(item, closest_location_id)
    item_details.append(details)

# find the 3 price points for each item
final_options = []
for detail in item_details:
    if detail is not None:
        no_data = ["NA", "NA", "NA"]
        data = detail["data"]

        prices = []
        for item in data:
            product_id = item["productId"]
            description = item["description"]
            price = item["items"][0]["price"]["regular"]
            locator = [product_id, description, price]
            prices.append(locator)

        n = len(prices)
        if n == 0:
            final_options.append("No items available.")
        elif n == 1:
            cheapest = prices[0]
            final_options.append([cheapest, no_data, no_data])
        elif n == 2:
            # Cheapest and most expensive will just be the two items
            sorted_prices = sorted(prices, key=lambda x: x[2])
            cheapest = sorted_prices[0]
            most_expensive = sorted_prices[1]
            final_options.append([cheapest, no_data, most_expensive])
        else:
            sorted_prices = sorted(prices, key=lambda x: x[2])
            cheapest = sorted_prices[0]
            most_expensive = sorted_prices[-1]
            middle_item = sorted_prices[n // 2]  # Median-ish
            final_options.append([cheapest, middle_item, most_expensive])
    else:
        final_options.append("No items available.")

print(final_options)







