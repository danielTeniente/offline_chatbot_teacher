from typing import List

def chunk_text(text: str, max_length: int = 300) -> List[str]:
    """
    Splits text into chunks of approximately `max_length` characters.
    """
    import textwrap
    return textwrap.wrap(text, max_length)