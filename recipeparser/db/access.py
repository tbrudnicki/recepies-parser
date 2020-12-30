def store_plan(db_file, plans):
    def _plan_to_db_recipe(plan):
        return ''

    def _store_recipe(recipe):
        pass

    for plan in plans:
        recipes = _plan_to_db_recipe(plan)
        for recipe in recipes:
            _store_recipe(recipe)
