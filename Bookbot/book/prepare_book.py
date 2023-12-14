BOOK_PATH = "book.txt"
book: dict[int, str] = {}
page_size = 300


def _get_part_text(text, start, page_size):
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
    

def prepare_book(path: str) -> None: 
    start=0  
    j=1 
    text_path=open(BOOK_PATH, encoding="utf8")
    text=text_path.read()
    while len(text)>start:
        text_list, text_len=_get_part_text(text , start, page_size)
        book[j] = text_list.lstrip()

        j+=1
        a=text_len
        start=start+a
    return book

print(prepare_book(BOOK_PATH))
