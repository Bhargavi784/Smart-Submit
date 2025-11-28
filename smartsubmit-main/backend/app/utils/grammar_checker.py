import fitz  # PyMuPDF for text extraction
import language_tool_python
import re

def check_pdf_grammar(file_path: str, max_issues: int = 10):
    """
    Extracts text from PDF and checks grammar using LanguageTool.
    Returns simplified top N grammar issues,
    filtering out names and uppercase words.
    """
    tool = language_tool_python.LanguageTool('en-US')
    doc = fitz.open(file_path)
    issues = []

    def is_name_or_uppercase(word):
        # Ignore all-uppercase words, names, or short capitalized words
        return (
            word.isupper() or
            (len(word) <= 3 and word[0].isupper()) or
            re.match(r"^[A-Z][a-z]+$", word)  # e.g., "Yash", "Sambhaji"
        )

    for i, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        if not text:
            continue

        matches = tool.check(text)
        for match in matches:
            error_text = text[match.offset:match.offset + match.errorLength].strip()

            # Filter out proper nouns or uppercase terms
            if not error_text or is_name_or_uppercase(error_text):
                continue

            suggestion = match.replacements[0] if match.replacements else None
            issues.append({
                "page": i,
                "error": match.message,
                "wrong": error_text,
                "suggestion": suggestion
            })

    # Limit to first N issues
    short_issues = issues[:max_issues]

    return {
        "total_issues": len(issues),
        "summary": [
            f"Page {i['page']}: '{i['wrong']}' → '{i['suggestion']}' ({i['error']})"
            for i in short_issues
        ]
    }
