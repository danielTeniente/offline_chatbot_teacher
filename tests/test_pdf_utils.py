import pytest
from pypdf import PdfWriter
from document_ingestion import pdf_utils


@pytest.fixture
def sample_pdf(tmp_path):
    """Create a sample PDF file for testing."""
    pdf_path = tmp_path / "sample.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(pdf_path, "wb") as f:
        writer.write(f)
    return str(pdf_path)


def test_get_dirs(tmp_path):
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    dirs = pdf_utils.get_dirs(str(tmp_path))
    assert "subdir" in dirs


def test_get_PDFs(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_text("dummy content")
    pdfs = pdf_utils.get_PDFs(str(tmp_path))
    assert any("test.pdf" in pdf for pdf in pdfs)


def test_get_PDF_numPages(sample_pdf):
    num_pages = pdf_utils.get_PDF_numPages(sample_pdf)
    assert num_pages == 1


def test_get_book_name():
    path = "/some/path/to/book.pdf"
    name = pdf_utils.get_book_name(path)
    assert name == "book"


def test_get_PDF_content(sample_pdf):
    content = pdf_utils.get_PDF_content(sample_pdf, 0)
    assert isinstance(content, str)


def test_has_selectable_text(sample_pdf):
    result = pdf_utils.has_selectable_text(sample_pdf)
    assert isinstance(result, bool)


def test_write_text(tmp_path):
    result = pdf_utils.write_text("Hello world", str(tmp_path), "output.txt")
    assert result
    output_file = tmp_path / "output.txt"
    assert output_file.exists()
    assert "Hello world" in output_file.read_text()


def test_get_paragraph():
    text = "This is a sample paragraph with the keyword inside. Another sentence with keyword again."
    phrase = "keyword"
    result = pdf_utils.get_paragraph(phrase, text)
    assert "KEYWORD" in result


def test_scan_book(sample_pdf):
    result = pdf_utils.scan_book(sample_pdf, "anything")
    assert isinstance(result, str)