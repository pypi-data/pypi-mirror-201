# buzzapi

An API client for the Agilix/Buzz LMS API

## Overview

The Agilix Buzz API is RESTful API for the Buzz LMS that accepts XML by default,
but can also accept and serve JSON. It consists of both paginated un-paginated
data, and requires a login token cookie for most endpoints.

The `buzzapi` package handles storing the login token as a cookie to be passed
with each request, as well as pagination on the relevant endpoints.

## Setup

```
from buzzapi import Client

# Creating a new client
client = Client("school/myusername", "mypassword")
```

## Examples

### Get resources from the GetUserActivityStream endpoint
```
client.get_user_activity_stream(12345, 54321) 
# => List of Activities
```

### Start IDLE with initialized client for testing
- Note that you will need to set the environment variables according to the .env_example
```
python -i buzzapi/client.py
```
