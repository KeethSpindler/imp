from discord import Embed
from imp_bot.models.drink_model import DrinkModel
from imp_bot.utils.colors import Colors

class DrinkEmbedder:
    """
    Embedder which creates and sets an embed with
    information from the Drink object
    """
    
    @staticmethod
    def get_embed(drink: DrinkModel, embed: Embed = None) -> Embed:
        embed = embed or Embed(
            title=drink.name,
            description="A drink for you, Sire...",
            color=Colors.DARK_NAVY.value,
        )
        embed.set_image(url=drink.drink_thumb)
        embed.add_field(name="Name", value=drink.name)
        embed.add_field(name="Category", value=drink.category)
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name="Alcoholic?", value=drink.is_alcoholic)
        embed.add_field(name="Glass Type", value=drink.glass)
        embed.add_field(name="\u200b", value="\u200b")
        ingredient_string = "\n".join(drink.ingredient_measurements)
        embed.add_field(name="Ingredients", value=ingredient_string, inline=False)
        embed.add_field(
            name="Instructions", value=drink.instructions, inline=False
        )
        embed.set_footer(
            text="Have ideas for additional functionality? Throw them in #robbot_discussion!"
        )
        return embed
