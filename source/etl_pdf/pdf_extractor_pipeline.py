from typing import List
from typing import Optional, Generator

import fitz


def read_pdf(file_path: str,
             start_index: Optional[int] = 0,
             page_count: Optional[int] = 1) -> Generator[str, None, None]:
    """
    Read text from a PDF file.

    Args:
        file_path (str): The path to the PDF file.
        start_index (Optional[int]): The index of the starting page (default is 0).
        page_count (Optional[int]): The number of pages to read (default is 1).

    Yields:
        str: Text content of each page in the specified range.
    """
    with fitz.open(file_path) as document:
        for index in range(start_index, (start_index + page_count)):
            page = document[index]
            yield page.get_text()


if __name__ == "__main__":
    file_path = "D:\\Books\\numpy reference.pdf"
    text: List[str] = []
    ls = list(read_pdf(file_path, 0, 5))
    for l in ls:
        print(len(l))
