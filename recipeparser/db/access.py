from itertools import chain
from recipeparser.db.model import Recipe, Ingredient

import sqlite3

insert_recipe = """insert into recipe(
    name,calories,recipe_type,instructions)
    values (?,?,?,?)
"""
insert_ingredient = """insert into ingredient(name, recipe_id,quantity,quantity_text) values (?,?,?,?)"""

populate_text_index = """insert into recipe_text_index(recipe_name, ingredients) values (?,?)"""


def text_index(recipe):
    return recipe.name, ','.join([ing.name for ing in recipe.ingredients])


def store_plans(db_file, plans):
    def _plan_to_db_recipe(plan):
        def parse_size(size_txt):
            return float(size_txt) if size_txt.isdigit() else None

        result = []
        for r in plan.a_recipes:
            ing = [Ingredient(i.name, parse_size(i.size), i.size) for i in r.ingredients]

            result.append(Recipe(r.recipe_name, float(plan.source_calories), r.instructions, ing, 'a'))

        for r in plan.b_recipes:
            ing = [Ingredient(i.name, parse_size(i.size), i.size) for i in r.ingredients]

            result.append(Recipe(r.recipe_name, float(plan.source_calories), r.instructions, ing, 'b'))

        return result

    def _store_recipe(recipe):

        cur.execute(insert_recipe, (recipe.name, recipe.calories, recipe.recipe_type, recipe.instruction))

        recipe_id = cur.lastrowid
        ii = []
        for i in recipe.ingredients:
            cur.execute(insert_ingredient, (i.name,recipe_id, i.quantity, i.quantity_text))
            ii.append(cur.lastrowid)

        cur.execute(populate_text_index, text_index(recipe))

    try:
        connection = sqlite3.connect(db_file)

        cur = connection.cursor()

        for plan in plans:
            recipes = _plan_to_db_recipe(plan)
            for recipe in recipes:
                _store_recipe(recipe)

        connection.commit()
    finally:
        if connection:
            connection.close()

