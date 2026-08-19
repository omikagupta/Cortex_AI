import re


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[str]:

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0"
        )

    if overlap < 0:
        raise ValueError(
            "overlap cannot be negative"
        )

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )


    # =================================================
    # Split document by numbered questions
    # Example:
    #
    # 1. Question...
    # 2. Question...
    # 3. Question...
    #
    # Each question + answer becomes a meaningful chunk
    # =================================================

    sections = re.split(
        r'(?=\n?\d+\.\s)',
        text,
    )


    chunks = []

    current_chunk = ""


    for section in sections:

        section = section.strip()


        if not section:
            continue


        # ---------------------------------------------
        # Add section if it fits current chunk
        # ---------------------------------------------

        if (
            len(current_chunk) + len(section)
            <= chunk_size
        ):

            current_chunk += (
                section
                + "\n\n"
            )


        else:

            # Save previous chunk

            if current_chunk:

                chunks.append(
                    current_chunk.strip()
                )


            # Start new chunk

            current_chunk = (
                section
                + "\n\n"
            )


    # ---------------------------------------------
    # Save remaining chunk
    # ---------------------------------------------

    if current_chunk:

        chunks.append(
            current_chunk.strip()
        )


    return chunks