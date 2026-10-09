# ---------- Validation ----------

def clean_choice(value, options, label):
    """Match input to one of the options, ignoring case and extra spaces."""
    for option in options:
        if str(value).strip().lower() == option.lower():
            return option
    raise ValueError(f"Invalid {label} '{value}'. Choose from: {', '.join(options)}.")


def clean_title(value):
    if not str(value).strip():
        raise ValueError("Title must not be blank.")
    return str(value).strip()


def clean_users(value):
    text = str(value).strip()
    if not (text.isascii() and text.isdigit()) or int(text) < 1:
        raise ValueError(f"Affected users must be a positive whole number (got '{value}').")
    return int(text)


# ---------- Priority (checked in order, first match wins) ----------

def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"