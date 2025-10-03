# Imp Changelog

## Types of changes

This changelog documents all notable changes made to the Imp project. The types of changes are categorized as follows:

- **Features**: New features or enhancements to existing functionality.
- **Updates**: Improvements or modifications to existing features.
- **Additions**: New components, modules, or dependencies added to the project.
- **Fixes**: Bug fixes or corrections to existing functionality.
- **Miscellaneous**: Other changes that do not fit into the above categories, such as

If a a category has no entries for a particular version, it will be omitted from that version's section.

***

## v1.1.0 - monkfishfillet on 2024-09-20

### Updates

- Overhauled Bartender cog to use slash commands
- Added commands for getting
  - a random drink
  - a drink by ingredient
  - alcoholic or non-alcoholic drinks
- Reworked the Drink model to implement Pydantic for data validation
- Added a DrinkList and DrinkListItem for better data handling of drink lists

### Additions

- Added `BaseClient` class for future API integrations
- Added `bartender_client.py` for `thecocktaildb` API interactions

***

## v1.0.0 - monkfishfillet on 2023-10-01

- Initial tag of Imp
