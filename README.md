# breadBot
breadBot is a Discord bot which generates bread recipes using randomisation of the types and distrbution of parameters such as flour, spices, enrichments and upload an HTML recipe and PNG preview upon being called. The compatibility of the combinations have been considered and the bot will only produce recipes that are sensible. Calcuations for grams are based on total flour grams and the recipe displays baker percentages.

![Alt text](readme_images/main.png?raw=true "Title")

## How to Use
- __Generating Recipes__: Once deployed, the bot can be called in a text channel using `!bread` and the bot will create and upload a recipe with total flour grams of 500g for the user to download.
- __Specifying Total Flour Amount__: The bot can be called using `!bread x`, where `x` will specify the total flour amount in grams for the recipe.
- __Randomized Recipe Names__: The user may modify `words.txt` to create a custom word list for bot to select from when generating recipes. Whitespace only lines will be ignored.
```
> ADJECTIVES\start\below
sampleAdjective

> NOUNS\start\below
sampleNoun
```

## Deployment on GNU/Linux
1. `git clone` the repository
2. Install `wkhtmltopdf` on your distribution for image previews. eg. `sudo apt install wkhtmltopdf`
2. Install `tmux` on your distribution for running the bot 24/7. eg. `sudo apt install tmux`
3. Create a Discord bot at the Discord Developer Portal and add the bot to your desired server
4. Use your Discord Bot Token to fill in the `.env` variable
5. Activate the virtualenv: `source env/bin/activate`
6. Run the bot using `tmux` so that it does not terminate on logout: 
   - `tmux`
   - `source env/bin/activate`
   - `python3 bot.py`
   - `Ctrl+b`, `d`
7. To shut down the bot:
   - `tmux`
   - `Ctrl+b`, `s`
   - select tmux session with the running bot
   - `x`, `y`