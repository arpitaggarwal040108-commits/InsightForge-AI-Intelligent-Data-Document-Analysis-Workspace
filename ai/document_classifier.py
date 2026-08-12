def classify_document(text):

    text = text.lower()

    if (
        "education" in text
        and "skills" in text
        and "experience" in text
    ):
        return "resume"

    elif (
        "abstract" in text
        and "methodology" in text
    ):
        return "research_paper"

    elif (
        "chapter" in text
        or "introduction" in text
    ):
        return "notes"

    else:
        return "general"