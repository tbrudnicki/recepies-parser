recipe_table_create = """CREATE TABLE IF NOT EXISTS recipe (
    id integer primary key,
    name text not null,
    calories float not null,
    recipe_type VARCHAR(10) not null,
    instructions text not null
    )
"""

ingredient_table_create = """CREATE TABLE IF NOT EXISTS ingredient (
    id integer primary key,
    name text not null,
    quantity float,
    quantity_text not null 
    )
"""
recipe_ingredient_table_create = """CREATE TABLE IF NOT EXISTS recipe_ingredient (
    id integer primary key,
    recepie_id integer,
    ingredient_id integer,
    foreign key (recepie_id) REFERENCES recipe(id),
    foreign key (ingredient_id) REFERENCES ingredient(id),
    )
"""

text_index_table_create = """CREATE VIRTUAL TABLE IF NOT EXISTS recipe_text_index 
    USING FTS5(recipe_name, ingredients)
"""


def initialize_db(cursor):
    cursor.execute(recipe_table_create)
    cursor.execute(ingredient_table_create)
    cursor.execute(recipe_ingredient_table_create)
    cursor.execute(text_index_table_create)
