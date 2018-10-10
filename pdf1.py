from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from PyPDF2.generic import TextStringObject
from PyPDF2.generic import NameObject
from PyPDF2.pdf import ContentStream
from PyPDF2.utils import b_

def any_match(text, match_list):
    # for keys in match_list:
    #     if all([key in text for key in keys]):
    #         return True
    if text == match_list:
        return True
    return False

class PdfTripper(object):
    
    def __init__(self, input_path, output_path, remove_list):
        self.reader = PdfFileReader(open(input_path, "rb"))
        self.writer = PdfFileWriter()
        self.output_path = output_path
        self.remove_list = remove_list

    def execute(self):
        self.process_content()
        self.writer.write(open(self.output_path, "wb"))

    def process_content(self):
        for page_num in range(self.reader.getNumPages()):
            page = self.reader.getPage(page_num)
            content_object = page["/Contents"].getObject()
            content = ContentStream(content_object, self.reader)
            for operands, operator in content.operations:
                if operator == b_("TJ") or operator == b_("Tj"):
                    text = operands[0]
                    if any_match(text, self.remove_list):
                        print (text)
                        operands[0] = TextStringObject('')
            page.__setitem__(NameObject('/Contents'), content)
            self.writer.addPage(page)


if __name__ == '__main__':
    input_path = "test.pdf"
    output_path = "test1.pdf"
    remove_list = []
    PdfTripper(input_path, output_path, remove_list).execute()