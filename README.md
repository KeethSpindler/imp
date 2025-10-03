# Imp v1.1.0

A Discord bot currently serving miscellaneous purposes, with plans to expand into a comprehensive Dungeons & Dragons utility tool.

## Features

### Current Features

#### 🍸 Bartender Cog - Drink Commands
Imp provides comprehensive drink recommendations through Discord slash commands:

- **`/drink random`** - Get a random drink recommendation from our extensive database
- **`/drink alcoholic`** - Find a random alcoholic beverage 
- **`/drink nonalcoholic`** - Discover a random non-alcoholic drink
- **`/drink ingredient <ingredient>`** - Search drinks by specific ingredients including:
  - Rum, Gin, Vodka, Tequila, Whiskey, Brandy, Bourbon, Scotch, Cognac
  - Absinthe, Amaretto, Kahlua, and more

Each command returns beautifully formatted embeds with:
- Drink name and image
-imp Category and glass type
- Alcoholic status
- Complete ingredient list with measurements
- Detailed preparation instructions

### Planned Features

Future versions will include D&D-focused functionality for both players and Dungeon Masters:

- **Character Management**: Character tracking, stats management, and progression
- **Item Database**: Comprehensive item descriptions and lookup system
- **Campaign Utilities**: Session planning tools and notes management
- **Combat Helpers**: Dice rolling, initiative tracking, and combat automation
- **World Building**: Location and NPC management tools

## Installation

### Prerequisites

- **Python 3.11+** (required by project configuration)
- A Discord Bot account ([Discord Developer Portal](https://discord.com/developers/applications))
- **[uv](https://github.com/astral-sh/uv)** package manager (recommended)
- OR pip (legacy support)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/imp.git
   cd imp
   ```

2. **Create Discord Application**
   - Visit the [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Navigate to the "Bot" section and create a bot
   - Copy both the Bot Token and Application ID

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   APPLICATION_ID=your_application_id_here
   ```
   
   **Security Note**: Never commit your `.env` file or share your tokens publicly.

4. **Install dependencies and run**

   Using uv (recommended):
   ```bash
   uv sync
   cd ./src
   uv run python -m imp_bot.bot
   ```

   Using pip:
   ```bash
   pip install -e .
   python src/imp_bot/bot.py
   ```

5. **Invite bot to server**
   - Use the Application ID from your environment variables
   - Visit: `https://discord.com/api/oauth2/authorize?client_id=YOUR_APP_ID&permissions=274877906944&scope=applications.commands%20bot`
   - Replace `YOUR_APP_ID` with your actual Application ID

## Architecture

Imp follows a modular Discord.py architecture with clean separation of concerns:

### Core Components

- **`imp_bot/bot.py`** - Main bot entry point with ImpBot class extending discord.ext.commands.Bot
- **`imp_bot/cogs/`** - Interactive command modules (currently: Bartender)
- **`imp_bot/models/`** - Pydantic data models for type safety and validation
- **`imp_bot/utils/`** - Utility modules organized by function:
  - **`clients/`** - HTTP clients for external API integration
  - **`embedders/`** - Discord embed formatting utilities  
  - **`colors/`** - Consistent color scheme management
  - **`formatters/`** - Data formatting utilities
  - **`sanitizers/`** - Input sanitization helpers
  - **`validators/`** - Input validation utilities

### Current Dependencies

- **discord.py** - Discord API wrapper for Python
- **pydantic** - Data validation using Python type annotations
- **httpx** - Modern HTTP client for asynchronous API calls
- **python-dotenv** - Environment variable management
- **aiohttp** - Additional async HTTP functionality

## Development

### Running in Development Mode

```bash
# Install in editable mode
uv sync
cd ./src
uv run python -m imp_bot.bot
```

### Adding New Cogs

1. Create a new cog file in `src/imp_bot/cogs/`
2. Follow the established pattern:
   ```python
   from discord.ext import commands
   
   class YourCog(commands.Cog):
       def __init__(self, bot):
           self.bot = bot
           
       # Your command methods here
   
   async def setup(bot):
       await bot.add_cog(YourCog(bot))
   ```
3. The bot automatically loads all `.py` files in the cogs directory

### Testing

Run the included test suite:
```bash
# Run tests with pytest
uv run pytest tests/

# Or run specific test files
uv run pytest tests/drinks/drink_model_test.ipynb
```

## Contributing

Imp welcomes contributions! Here's how you can help:

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/imp.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `uv sync`
5. Make your changes following the existing code patterns

### Pull Request Guidelines

- Ensure your code follows the existing style and structure
- Add tests for new functionality
- Update documentation as needed
- Test your changes thoroughly before submitting

### Areas for Contribution

- Additional drink database integrations
- New utility commands and cogs
- D&D feature development (character sheets, dice rolling, etc.)
- Documentation improvements
- Test coverage expansion

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed information about changes and updates to Imp.

---

**Note**: Imp is actively developed and may have breaking changes between versions. Check the changelog before updating.