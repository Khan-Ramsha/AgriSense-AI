import re
def truncate_response(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    if not text.strip().endswith(('.', '!', '?')):
        sentences = sentences[:-1]
    return ' '.join(sentences).strip()
