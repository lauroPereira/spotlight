def clean_texts(texts):
    return [t.strip().lower() for t in texts if isinstance(t, str)]