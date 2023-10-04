import re


def filter_including_sentences(text: str) -> str:
    stop_items = [".", "!", ";"]
    pattern = r', including[^' + ''.join(stop_items) + ']*?(?=[' + ''.join(stop_items) + '])'
    return re.sub(pattern, '', text)

