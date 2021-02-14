class Recipe:
    def __init__(self, name, calories, instruction, ingredients, recipe_type):
        self.name = name.replace('\n', ' ')
        self.calories = calories
        self.instruction = instruction
        self.ingredients = ingredients
        self.recipe_type = recipe_type


class Ingredient:
    def __init__(self, name, quantity, quantity_text):
        self.name = name.replace('\n', ' ')
        self.quantity = quantity
        self.quantity_text = quantity_text
