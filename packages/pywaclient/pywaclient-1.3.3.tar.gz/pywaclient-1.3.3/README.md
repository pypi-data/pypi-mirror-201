# World Anvil API Python Client [WIP]

I am currently in the process of adapting the library to the next
version of the API. This next version is not public yet. If you wish to 
get access please message the team to discuss it.

The latest version which works with Aragorn is `0.12.1`. Use the 
highest tag to work with Boromir.

The World Anvil API provides endpoints to interact with the World Anvil database.

[Aragorn API Documentation](https://www.worldanvil.com/api/aragorn/documentation)
## Installation
The package is published on PYPI and can be installed with pip.

`pip --install pywaclient`

## Usage
This is a simple example on how to use the endpoints.

```python
import os
from pywaclient.api import BoromirApiClient

client = BoromirApiClient(
    '<YourScriptName>',
    '<link-to-your-website-or-bot-repository>', '<version>', os.environ['WA_APPLICATION_KEY'],
    os.environ['WA_AUTH_TOKEN']
)

# get your own user id. It is not possible to discover the user ids of other users via the API.
authenticated_user = client.user.identity()

# get the references to all the worlds on your account.
worlds = [world for world in client.user.worlds(authenticated_user['id'])]

# get the references to all the category on the first world.
categories = [category for category in client.world.categories(worlds[0]['id'])]

# gets a list of all the articles without a category in the first world
articles = [article for article in client.category.articles(worlds[0]['id'], '-1')]

# gets the full content of the first article
article = client.article.get(articles[0]['id'], 2)

# gets the full content of the first category. Categories and most other resources do not have a granularity of 2.
category = client.category.get(categories[0]['id'], 1)
```

