import os
import asyncio
from dotenv import load_dotenv
from discord import Intents
from discord.ext.commands import Bot, Context
from imp_bot import __version__

load_dotenv()

COGS_DIR = "./imp_bot/cogs"
FILES = [
    file
    for file in os.listdir(COGS_DIR)
    if file.endswith(".py") and not file.startswith("__")
]

# 1. Create a custom class that inherits from commands.Bot
class ImpBot(Bot):
    def __init__(self):
        # Define intents and pass everything to the parent class
        intents = Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix="/", 
            intents=intents, 
            application_id=os.getenv("APPLICATION_ID")
        )

    async def load_all_cogs(self):
        print("Loading Cogs...")
        for file in FILES:
            extension_name = f"imp_bot.cogs.{file[:-3]}"
            await self.load_extension(extension_name)
            print(f"- '{file[:-3]}' extension loaded")

    async def unload_all_cogs(self):
        print("Unloading Cogs...")
        for file in FILES:
            extension_name = f"imp_bot.cogs.{file[:-3]}"
            await self.unload_extension(extension_name)
            print(f"- '{file[:-3]}' extension unloaded")

    # 2. Override the setup_hook method for reliable async setup
    async def setup_hook(self) -> None:
        # This runs after the bot is ready but before it connects.
        
        # 3. Load all your cogs first
        await self.load_all_cogs()
        
        # 4. Sync the command tree to Discord.
        # This registers all your slash commands found in the cogs.
        synced = await self.tree.sync()
        print(f"Synced {len(synced)} command(s).")

    # 5. (Recommended) Move events into the class
    async def on_ready(self):
        print("-" * 30)
        print(f"Imp v{__version__} is now running.")
        print(f"{self.user} is ready to serve, Master.")
        print("-" * 30)

# Main execution block
async def main():
    # 6. Instantiate your new bot class
    bot = ImpBot()
    
    # (Recommended) Move the refresh command into the class or a dedicated cog
    # For simplicity, I'll redefine it here pointing to the bot's methods.
    @bot.command(name="refresh", hidden=True)
    async def refresh(ctx: Context):
        print("\nReloading Cogs via command...")
        await bot.unload_all_cogs()
        await bot.load_all_cogs()
        await bot.tree.sync() # Re-sync after reloading
        print("Cogs reloaded and commands re-synced successfully.")
        await ctx.message.add_reaction("👍")

    await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())