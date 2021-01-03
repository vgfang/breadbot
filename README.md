# breadBot
breadBot is a Discord bot which generates bread recipes using randomisation of the types and distrbution of parameters such as flour, spices, enrichments and upload an HTML recipe upon being called. The compatibility of the combinations have been considered and the bot will only produce recipes that are sensible.

## How to Use
- __Generating Recipes__: Once deployed, the bot can be called in a text channel using `!bread` and the bot will create and upload an HTML recipe with total flour grams of 500g for the user to download.
- __Specifying Total Flour Amount__: The bot can be called using `!bread x`, where `x` will specify the total flour amount in grams for the recipe.
- __Randomized Recipe Names__: The user may modify `words.txt` to create a custom word list for bot to select from when generating recipes.

## Deployment
1. `git clone` the repository
2. Create a Discord bot at the Discord Developer Portal and add the bot to your desired server
3. Use your Discord Bot Token and Discord Guild Token to fill in the `.env` variables
4. Activate the virtualenv: `source env/bin/activate`
5. Run the bot as a background process: `python3 bot.py &`