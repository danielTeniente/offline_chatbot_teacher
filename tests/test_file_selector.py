import pytest
import os
from unittest.mock import patch
from document_ingestion import file_selector

@patch("document_ingestion.file_selector.Path.rglob")
@patch("document_ingestion.pdf_utils.has_selectable_text")
def test_discover_books(mock_has_text, mock_rglob):
    from pathlib import Path

    mock_pdf_path = Path("/fake/path/sample.pdf")
    mock_rglob.return_value = [mock_pdf_path]
    mock_has_text.return_value = True

    result = file_selector.discover_books("/fake/path")
    assert "sample.pdf" in result
    assert result["sample.pdf"]["name"] == "sample.pdf"
    assert os.path.normpath(result["sample.pdf"]["path"]) == os.path.normpath("/fake/path/sample.pdf")
    assert result["sample.pdf"]["has_selectable_text"] is True