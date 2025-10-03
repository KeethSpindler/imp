from imp_bot.utils.sanitizers.base_sanitizer import BaseSanitizer

class DrinkSanitizer(BaseSanitizer):
    """
    Drink Sanitizer which returns a sanitized version of the drink
    json passed into it
    """

    def __init__(self, json: dict):
        BaseSanitizer.__init__(self, json)

    def clean_json(self):
        drink_dict = {}
        for key in self.filth:
            if self.filth[key] != None:
                drink_dict[key] = self.filth[key]

        return drink_dict