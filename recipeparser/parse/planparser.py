import camelot
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1

from recepieparser.model.data import Recipe, Ingredient, Plan


class PlanParser:
    class ParsingContext:
        def __init__(self, tables, position=0):
            self.tables = tables
            self.position = position

    class RecipesSectionParser:
        def __init__(self, context):
            self.context = context

        def parse(self):
            recipes = []
            for i in range(self.context.position, len(self.context.tables)):
                current_table = self.context.tables[i]

                if "Przepis" in current_table.data[1][0]:
                    recipes.append(self._parse_table(current_table))

            return recipes, PlanParser.ParsingContext(self.context.tables, i + 1)

        def _parse_table(self, table):
            row, col = table.shape
            recipe_name = table.data[0][0]
            r = Recipe(recipe_name)
            instructions = []
            ingredients = []
            for i in range(2, row):
                instructions.append(table.data[i][0])
                ingredient_name = table.data[i][1]
                ingredient_size = table.data[i][2]
                r.append_ingredient(Ingredient(ingredient_name, ingredient_size))

            r.set_instructions(''.join(instructions))

            return r

    class CaloriesParser:
        def __init__(self, context):
            self.context = context

        def parse(self):
            for i in range(self.context.position, len(self.context.tables) + 1):
                t = self.context.tables[i]
                if "Kaloryczno" in t.data[0][0]:
                    return PlanParser.extract_calories_number(t.data[1][0]), PlanParser.ParsingContext(
                        self.context.tables, i + 1)

            return None, PlanParser.ParsingContext(self.context.tables, i + 1)

    def __init__(self):
        pass

    def parse(self, file_name):
        with(open(file_name, 'rb')) as pdf_file:
            parser = PDFParser(pdf_file)
            document = PDFDocument(parser)
            page_count = resolve1(document.catalog['Pages'])['Count']

        # print(self._generate_pages(page_count))

        tables = camelot.read_pdf(file_name, pages=self._generate_pages(page_count))
        return self._extract_plan(tables)

    def _extract_plan(self, tables):
        calories_parser = PlanParser.CaloriesParser(PlanParser._initial_context(tables))

        calories, continuation_context = calories_parser.parse()
        recipes_parser = PlanParser.RecipesSectionParser(continuation_context)
        recipes, context = recipes_parser.parse()

        section_a = recipes[:3]
        section_b = recipes[3:]

        p = Plan(calories)
        p.set_section_a(section_a)
        p.set_section_b(section_b)
        return p

    @staticmethod
    def _initial_context(tables):
        return PlanParser.ParsingContext(tables)

    @staticmethod
    def _generate_pages(page_count):
        return ','.join([str(i) for i in range(1, page_count + 1)])

    @staticmethod
    def extract_calories_number(text_field):
        return next(float(i) for i in text_field.split(' ') if i.isdigit())
