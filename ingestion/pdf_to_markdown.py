import pymupdf4llm
import tempfile
import os


def convert_pdf_to_markdown(pdf_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    try:
        md_text = pymupdf4llm.to_markdown(tmp_path)
        return md_text
    finally:
        os.unlink(tmp_path)
