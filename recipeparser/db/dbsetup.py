import sqlite3

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
    recipe_id integer,
    name text not null,
    quantity float,
    quantity_text not null,
    foreign key (recipe_id) REFERENCES recipe(id) ON DELETE CASCADE 
         ON UPDATE NO ACTION 
    )
"""


text_index_table_create = """CREATE VIRTUAL TABLE IF NOT EXISTS recipe_text_index 
    USING FTS5(recipe_name, ingredients)
"""


def initialize_db(db_path):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(recipe_table_create)
        cursor.execute(ingredient_table_create)
        cursor.execute(text_index_table_create)

        connection.commit()
    finally:
        if connection:
            connection.close()
