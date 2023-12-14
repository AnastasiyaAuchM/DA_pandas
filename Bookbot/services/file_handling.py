import os
import sys


BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


# The function that returns a string with the text of the page and its size
def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    end = min(start + page_size, len(text)) 
    for i in range(end, start, -1):
        if text[i - 1] in ".,!;:?" and i==len(text):
            break
        elif text[i - 1] in ".,!;:?" and text[i-2] in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' and text[i] in (' ', '\n'):
            break
        else:
            continue
            
    else:
        i = end
    page = text[start:i].rstrip()
    return page, len(page)


# The function that fills the dictionary 
def prepare_book(path: str) -> None:
    start=0  
    j=1 
    text_path=open(BOOK_PATH, encoding="utf8")
    text=text_path.read()
    while len(text)>start:
        text_list, text_len=_get_part_text(text , start, 1050)
        book[j] = text_list.lstrip()

        j+=1
        a=text_len
        start=start+a
    return book


# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))

