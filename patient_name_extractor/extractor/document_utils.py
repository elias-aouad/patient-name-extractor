from patient_name_extractor.extractor.interfaces import Document, Word


def group_words_into_lines(
    words: list[Word], y_tolerance: float = 0.005
) -> list[list[Word]]:
    """
    All words on the same line
    """
    lines = []
    current_line = []
    last_y = None

    for w in words:
        if last_y is None or abs(w.bbox.y_min - last_y) <= y_tolerance:
            current_line.append(w)
        else:
            lines.append(current_line)
            current_line = [w]
        last_y = w.bbox.y_min

    if current_line:
        lines.append(current_line)
    return lines


def reconstruct_text_from_document(
    document: Document, y_tolerance: float = 0.005
) -> str:
    pages: list[str] = []
    for page in document.pages:
        words = list(page.words)

        # Sort words vertically, then horizontally
        words.sort(key=lambda w: (w.bbox.y_min, w.bbox.x_min))

        # Group words into lines
        lines = group_words_into_lines(words=words, y_tolerance=y_tolerance)

        # Join words inside lines
        reconstructed_lines = []
        for line in lines:
            line.sort(key=lambda w: w.bbox.x_min)
            reconstructed_lines.append(" ".join([w.text for w in line]))

        # update page text
        text = "\n".join(reconstructed_lines)
        pages.append(text)

    return "\n\n".join(pages)
