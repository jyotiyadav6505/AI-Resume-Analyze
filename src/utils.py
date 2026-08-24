def clean_text(text):
    """Clean unnecessary spaces and blank lines from text."""

    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def format_analysis(analysis):
    """Prepare AI analysis for display."""

    if not analysis:
        return "No analysis available."

    return analysis.strip()