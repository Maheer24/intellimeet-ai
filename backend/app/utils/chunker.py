
def fixed_size_chunk_with_overlap(
    text: str, overlap: int, chunk_size: int
) -> list[str]:
    """
    Splits text into fixed sized chuncks with overlap
    """
    if chunk_size <= 0:
        raise ValueError("chunk size must be greater than 0")
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk")

    chunks_list = []
    start_index = 0
    words = text.split()
    len_text = len(words)

    while start_index < len_text:
        # if end_index becomes larger then len_text consider len_text as the end_index
        end_index = min(start_index + chunk_size, len_text)

        chunk = words[start_index:end_index]
        chunks_list.append(
            " ".join(chunk)
        )  # " ".join(chunk) -> concatenates words in chunk into a single string

        if end_index == len_text:
            break

        start_index = end_index - overlap

    return chunks_list

