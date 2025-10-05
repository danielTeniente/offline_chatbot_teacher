import os
import json
import re
import cv2
import pdf2image
import pytesseract
import os
import json
from shutil import Error
from typing import List, Tuple
from .pdf_utils import get_PDF_numPages, get_book_name, get_paragraph
from typing import List


def sanitize_name(name: str) -> str:
    """
    Removes all non-alphanumeric characters from the given string.
    Useful for creating safe filenames or folder names.
    """
    return re.sub(r'[^a-zA-Z0-9]', '', name)


def there_are_imgs(book_path: str) -> bool:
    """
    Checks if the first page image of the book already exists.
    """
    book_img_name = get_book_name(book_path) + '_page_1.jpg'
    imgs_folder = 'book_imgs'
    return os.path.isfile(os.path.join(imgs_folder, book_img_name))


def create_book_images(book_path: str, output_folder: str = 'book_imgs') -> bool:
    """
    Converts each page of the PDF book into a JPEG image and saves them.
    Returns True if successful, False otherwise.
    """
    try:
        pages = pdf2image.convert_from_path(pdf_path=book_path, dpi=350)
        book_img_name = get_book_name(book_path)
        imgs_folder = output_folder
        os.makedirs(imgs_folder, exist_ok=True)

        for i, page in enumerate(pages):
            current_page = i + 1
            book_img_path = os.path.join(imgs_folder, f"{book_img_name}_page_{current_page}.jpg")
            page.save(book_img_path, "JPEG")

        return True
    except Error:
        return False



def mark_region(image_path: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Detects and returns bounding boxes of text regions in the image.
    """
    im = cv2.imread(image_path)
    if im is None:
        # Handle the error appropriately for GUI (e.g., log or raise)
        return []

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 30)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)
    cnts, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    line_items_coordinates = []
    if not cnts:
        return line_items_coordinates

    last_y = cv2.boundingRect(cnts[0])[1]
    for i, c in enumerate(cnts):
        x, y, w, h = cv2.boundingRect(c)
        if ((y - last_y) ** 2 < 25 and i > 0):
            last_c = line_items_coordinates[-1]
            lx = last_c[0][0]
            line_items_coordinates[-1] = [(lx, y), (x + w, y + h)]
        else:
            line_items_coordinates.append([(x, y), (x + w, y + h)])
        last_y = y

    return line_items_coordinates



def ocr_img(img_path: str) -> str:
    """
    Performs OCR on the image and returns extracted text.
    Loads Tesseract executable path from ../config.json.
    """
    # Resolve path to config.json in the parent directory
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    config_path = os.path.abspath(config_path)

    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            tesseract_path = config.get("tesseract_cmd", "")
            if tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
    except (FileNotFoundError, json.JSONDecodeError):
        return "Error: Tesseract path not configured properly."

    paragraphs = mark_region(img_path)
    image = cv2.imread(img_path)

    if image is None:
        return "Error: Image could not be loaded."

    text = ''
    for pi in paragraphs:
        upleft_corner = pi[0]
        downright_corner = pi[1]
        img = image[upleft_corner[1]:downright_corner[1], upleft_corner[0]:downright_corner[0]]
        if img is not None and 0 not in img.shape:
            _, thresh1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
            text += pytesseract.image_to_string(thresh1, config='--psm 6')

    return text


def scan_book_with_OCR(path: str, phrase: str) -> str:
    """
    Scans a PDF book using OCR, caches the text, and searches for a phrase.
    Returns contextual matches with page numbers.
    """
    num_pages = get_PDF_numPages(path)
    book_name = get_book_name(path)
    sanitized_book_name = sanitize_name(book_name)

    base_txt_folder = 'book_txt'
    book_txt_folder = os.path.join(base_txt_folder, sanitized_book_name)

    os.makedirs(base_txt_folder, exist_ok=True)
    os.makedirs(book_txt_folder, exist_ok=True)

    if not there_are_imgs(path):
        if not create_book_images(path):
            return 'OCR scanning failed for this book.'

        imgs_folder = 'book_imgs'
        for page in range(num_pages):
            current_page = page + 1
            image_file = os.path.join(imgs_folder, f"{book_name}_page_{current_page}.jpg")
            txt_file = os.path.join(book_txt_folder, f"{book_name}_page_{current_page}.txt")

            book_content = ocr_img(image_file)
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(book_content)
            os.remove(image_file)

    info = ''
    for page in range(num_pages):
        current_page = page + 1
        txt_file = os.path.join(book_txt_folder, f"{book_name}_page_{current_page}.txt")
        if os.path.exists(txt_file):
            with open(txt_file, 'r', encoding='utf-8') as f:
                book_content = f.read()
        else:
            book_content = ""
        match = get_paragraph(phrase, text=book_content)
        if match:
            info += f'Página {current_page}\n...{match}...\n\n'

    return info




