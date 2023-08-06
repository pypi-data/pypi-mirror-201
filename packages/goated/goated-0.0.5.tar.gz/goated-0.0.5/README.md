# Goated Python Library

A handy library to interacting with, sourcing information from and trading on the Goated Exchange.

## Creating an authenticated Client to interact with the API using email and password

```
from goated.client import TradingClient

# Create a Goated Client Object to interact with the API
client = TradingClient.create_with_login(
    url = "https://api.goated.com",
    email = "YOUR_GOATED_EMAIL",
    password = "YOUR_GOATED_PASSWORD"
)

```

## Or using API Key and Secret (available from account tab)

```
from goated.client import TradingClient

# Create a Goated Client Object to interact with the API
client = TradingClient.create_with_api_key(
    url = "https://api.goated.com",
    api_key = "YOUR_GOATED_API_KEY",
    api_secret = "YOUR_GOATED_API_SECRET"
)

```

## Creating a State container, sourcing and loading some user information into the container

```
# Create a State Container object to hold relational state
state = Container()

# Get balances response from API
balances_response = client.get_balances()
# Add/update it within the state container
state.update_balances(balances_response)

# Get positions response from API
positions_response = client.get_positions() # Without any filters
# Add/update it within the state container
state.update_positions(positions_response)

# Get orders response from API
orders_response = client.get_orders() # Without any filters
# Add/update it within the state container
state.update_orders(orders_response)

print(state.__dict__)

```

## Sourcing information from the API 

```
# Get all categories
categories = client.get_categories()  # Without any filters

print('Categories:')
print(categories)

# Get subcategory record for first category
category_id = categories[0].get('id')
subcategories = client.get_subcategories(
    category_ids=[category_id]
) if category_id != None else []
print('Subcategories:')
print(subcategories)

# Get events in the first subcategory
subcategory_id = subcategories[0].get('id') if len(subcategories) > 0 else None
events = client.get_events(
    subcategory_ids=[subcategory_id]
) if subcategory_id != None else []
print('Events:')
print(events)

# Get all markets in the first event
event_id = events[0].get('id') if len(events) > 0 else None
markets = client.get_markets(
    event_id=[event_id]
) if event_id != None else []
print('Markets:')
print(markets)


```

