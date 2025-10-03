from imp_bot.utils.formatters.base_formatter import BaseFormatter

class DrinkFormatter(BaseFormatter):
    """
    Drink Formatter which formats the ingredient's
    and measurements of a drink
    """
    def __init__(self, json: dict):
        if isinstance(json, dict) != True:
            raise TypeError("The argument must be of type dict")
        BaseFormatter.__init__(self, json)
        self.ingredients_string = self.make_ingredients_string(self.arg)

    def make_ingredients_string(self, json):
        ingredients = [
            json.get(ing)
            for ing in json
            if "Ingredient" in ing and json.get(ing) is not None
        ]
        measurements = [
            json.get(measure)
            for measure in json
            if "Measure" in measure and json.get(measure) is not None
        ]

        if len(measurements) == 0:
            return ingredients

        ingredient_list = []
        for i in range(len(ingredients)):
            if i < len(measurements):
                ingredient_list.append(measurements[i].strip() + " " + ingredients[i])
            elif ingredients[i] == " ":
                pass
            else:
                ingredient_list.append(ingredients[i])
        return ingredient_list