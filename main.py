import os
import sqlite3

from recipeparser.db.access import store_plans
from recipeparser.parse.planparser import PlanParser
from recipeparser.db.dbsetup import initialize_db
import pkg_resources


def generate_pages(page_count):
    return ','.join([str(i) for i in range(1, page_count + 1)])


def main():
    data_directory = pkg_resources.resource_filename('recipeparser', 'data/')
    plans = []
    for root, dirs, files in os.walk(data_directory, topdown=False):

        for file in files:
            if file.endswith('pdf'):
                absolute_path = os.path.join(root, file)
                print(f'Processing file: {absolute_path}')
                parser = PlanParser()
                plan = parser.parse(absolute_path)
                plans.append(plan)
    print(len(plans))

    db_directory = pkg_resources.resource_filename('recipeparser', 'data/db')
    db_path = os.path.join(db_directory, 'recipes.db')
    initialize_db(db_path)
    store_plans(db_path, plans)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
