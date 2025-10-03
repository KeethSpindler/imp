import traceback
from typing import Optional, Literal
from discord import app_commands, Interaction
from discord.ext import commands
from discord.ext.commands import Bot
from imp_bot.models.drink_model import DrinkModel
from imp_bot.utils.clients.bartender_client import BartenderClient
from imp_bot.utils.embedders import DrinkEmbedder
from imp_bot.utils.validators import validate_drink_args

INGREDIENTS = ["rum", "gin", "vodka", "tequila", "whiskey", "brandy", "bourbon", "scotch", "cognac", "absinthe", "amaretto", "kahlua"]
STAND_ALONE_ARGS = ["-a", "-na", "-h"]
VALUE_ARGS = {"-i": INGREDIENTS}

class Bartender(
    commands.GroupCog,  # Inherit from GroupCog
    group_name="drink", # Define the group name here
    name="Bartender",
    description="Bartender serves up a random alcoholic or nonalcoholic drink!",
):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def _handle_interaction_drink_request(self, interaction: Interaction, drink_fetcher: callable, value: str = None):
        try:
            await interaction.response.defer()
            response = await drink_fetcher() if not value else await drink_fetcher(value)
            drink_json = response.get("drinks", [None])[0]

            if not drink_json:
                await interaction.followup.send("Apologies, sire, something went wrong fetching your drink.")
                return

            drink_model = DrinkModel.model_validate(drink_json)
            drink_embed = DrinkEmbedder.get_embed(drink_model)
            await interaction.followup.send(embed=drink_embed)
        except Exception as ex:
            traceback.print_exc()
            await interaction.followup.send(f"Ayo, your code is wack.\n Error: {ex}")

    @app_commands.command(name="random", description="Get a random drink recommendation")
    async def drink_random(self, interaction: Interaction):
        await self._handle_interaction_drink_request(interaction, BartenderClient().get_random_drink_json)
    
    @app_commands.command(name="alcoholic", description="Get a random alcoholic drink")
    async def drink_alcoholic(self, interaction: Interaction):
        await self._handle_interaction_drink_request(interaction, BartenderClient().get_alcoholic_drinks)
    
    @app_commands.command(name="nonalcoholic", description="Get a random non-alcoholic drink")
    async def drink_nonalcoholic(self, interaction: Interaction):
        await self._handle_interaction_drink_request(interaction, BartenderClient().get_non_alcoholic_drinks)
    
    @app_commands.command(name="ingredient", description="Get a drink with a specific ingredient")
    @app_commands.describe(ingredient="Choose an ingredient for your drink")
    @app_commands.choices(ingredient=[
        app_commands.Choice(name=ingredient.capitalize(), value=ingredient)
        for ingredient in INGREDIENTS
    ])
    async def drink_ingredient(self, interaction: Interaction, ingredient: str):
        await self._handle_interaction_drink_request(
            interaction, 
            BartenderClient().get_drink_list_by_ingredient, 
            ingredient
        )

async def setup(bot: Bot):
    await bot.add_cog(Bartender(bot))