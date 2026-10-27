def chunk_text(text: str, size:int, overlap: int) -> list[str]:
    """
    Splits the input text into chunks of specified size.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The maximum size of each chunk.

    Returns:
        list[str]: A list of text chunks.
    """

    if size <=0:
        raise ValueError("size must be a positive integer")
    if not 0<= overlap < size:
        raise ValueError("overlap must be a non-negative integer less than size")

    words = text.split()
    if not words:
        return []

    step = size - overlap
    chunks = []
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + size])
        chunks.append(chunk)
        if i + size >= len(words):
            break
    return chunks
