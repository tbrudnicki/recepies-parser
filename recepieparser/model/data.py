class Ingredient:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'{self.name}({self.size})'


class Recipe:
    def __init__(self, name):
        self.recipe_name = name
        self.ingredients = []
        self.instructions = ''

    def set_instructions(self, instruction_text):
        self.instructions = instruction_text

    def append_ingredient(self, ingredient):
        self.ingredients.append(ingredient)


class Plan:
    def __init__(self, calories):
        self.source_calories = calories
        self.a_recipes = set()
        self.b_recipes = set()

    def append_a_recipe(self, recipe):
        self.a_recipes.add(recipe)

    def append_b_recipe(self, recipe):
        self.b_recipes.add(recipe)

    def set_section_a(self, recipes):
        self.a_recipes.update(recipes)

    def set_section_b(self, recipes):
        self.b_recipes.update(recipes)
