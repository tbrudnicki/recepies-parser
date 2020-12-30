import camelot
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import resolve1
import os

from recepieparser.parse.planparser import PlanParser
import pkg_resources


def generate_pages(page_count):
    return ','.join([str(i) for i in range(1, page_count + 1)])


def main():
    data_directory = pkg_resources.resource_filename('recepieparser', 'data/')
    plans = []
    for root, dirs, files in os.walk(data_directory, topdown=False):
        for file in files:
            absolute_path = os.path.join(root, file)
            print(f'Processing file: {absolute_path}')
            parser = PlanParser()
            plan = parser.parse(absolute_path)
            plans.append(plan)
    print(len(plans))

    #
    # i = 0
    # output = StringIO()
    # with open('/ubuntu-data/Downloads/TBR-3000_1.pdf', 'rb') as pdf_file:
    #     extract_text_to_fp(pdf_file, output, laparams=LAParams(), output_type='html', codec=None)
    #
    # with open('/ubuntu-data/Downloads/example.html', 'a') as html_file:
    #     html_file.write(output.getvalue())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
