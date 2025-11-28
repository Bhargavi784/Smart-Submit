import fitz
from typing import Dict

def check_pdf_margins(file_path: str, required_margins: Dict[str, float]) -> Dict:
    """
    Accurate PDF margin checker using text spans instead of raw blocks.
    Detects left, right, and top margins based on visible text glyphs.
    Ignores invisible and whitespace elements.
    """

    doc = fitz.open(file_path)
    report = []
    format_ok = True

    # Default margins (in inches)
    req_left = required_margins.get("left", 1.25)
    req_right = required_margins.get("right", 1.0)
    req_top = required_margins.get("top", 1.0)

    for i, page in enumerate(doc, start=1):
        rect = page.rect
        width, height = rect.width, rect.height

        # Extract word-level bounding boxes (more precise than blocks)
        words = page.get_text("words")  # [x0, y0, x1, y1, word, block_no, line_no, word_no]
        if not words:
            report.append(f"Page {i}: No text detected")
            format_ok = False
            continue

        # Filter out invisible / tiny words
        valid_words = [w for w in words if (w[2] - w[0]) > 5]
        if not valid_words:
            report.append(f"Page {i}: No visible text detected")
            format_ok = False
            continue

        x0 = min(w[0] for w in valid_words)
        x1 = max(w[2] for w in valid_words)
        y0 = min(w[1] for w in valid_words)

        # Convert to inches
        left_margin = round(x0 / 72, 2)
        right_margin = round((width - x1) / 72, 2)
        top_margin = round(y0 / 72, 2)

        issues = []

        # Left margin check (important)
        if left_margin < req_left - 0.1:
            issues.append(f"Left margin too small ({left_margin} in, expected ≥ {req_left} in)")
        elif left_margin > req_left + 0.2:
            issues.append(f"Left margin too large ({left_margin} in, expected ~{req_left} in)")

        # Right margin check (too narrow)
        if right_margin < req_right - 0.1:
            issues.append(f"Right margin too small ({right_margin} in, expected ≥ {req_right} in)")

        # Top margin check (too small / large)
        if top_margin < req_top - 0.1:
            issues.append(f"Top margin too small ({top_margin} in, expected ≥ {req_top} in)")
        elif top_margin > req_top + 0.5:
            issues.append(f"Top margin too large ({top_margin} in, expected ~{req_top} in)")

        if issues:
            format_ok = False
            for issue in issues:
                report.append(f"Page {i}: {issue}")

    return {
        "format_ok": format_ok,
        "report": report
    }
