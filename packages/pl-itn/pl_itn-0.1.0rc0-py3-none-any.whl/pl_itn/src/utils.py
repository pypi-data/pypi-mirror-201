import re
from string import punctuation


def pre_process(text: str):
    text = text.lower()

    # Add spaces around punctuation
    for punct in punctuation:
        text = text.replace(punct, f" {punct} ")

    # Remove multiple spaces
    text = re.sub(r" +", " ", text)
    text = text.strip()
    return text


def post_process(text: str):
    text = re.sub(r" +", " ", text)
    text = text.strip()
    return text
