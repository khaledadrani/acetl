from typing import Optional

import fitz


class PdfExtractorPipeline:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.document: Optional[fitz.Document] = None
        self.page = None
        self.text = None

    def extract(self):
        self.document = fitz.open(self.file_path)  # should with better

    def transform(self):
        self.page = self.document.load_page(1)

    def load(self):
        self.text = str(self.page)
        self.document.close()

    def __call__(self):
        self.extract()
        self.transform()
        self.load()
        return self.text
