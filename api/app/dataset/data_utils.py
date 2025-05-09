import re
from pyvi.ViTokenizer import tokenize


def preprocess(text, remove_nl=False):
    # Remove all newlines and tabs
    if remove_nl:
        text = text.replace("\n", " ").replace("\t", " ")
    # Clean certain special characters
    text = (
        text.replace("“", '"')
        .replace("”", '"')
        .replace("‘", "'")
        .replace("’", "'")
        .replace("_", "-")
        .replace(".", " ")
    )
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Lowercase the text
    text = text.lower()

    return text.strip()


def process_and_tokenize(text, tokenizer, max_length):
    unk_token = tokenizer.unk_token
    sep_token = tokenizer.sep_token
    cls_token = tokenizer.cls_token
    pas_token_id = tokenizer.pad_token_id

    text = preprocess(text)

    text = tokenize(text)

    text = text.split()

    tokens = []

    for word in text:
        word_tokens = tokenizer.tokenize(word)
        if not word_tokens:
            tokens.append(unk_token)
        else:
            tokens.extend(word_tokens)

    if len(tokens) > max_length - 2:
        tokens = tokens[: max_length - 2]

    # Add [CLS] and [SEP] tokens
    tokens = [cls_token] + tokens + [sep_token]

    # Convert tokens to IDs
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    attn_mask = [1] * len(input_ids)

    padding_length = max_length - len(input_ids)
    if padding_length > 0:
        input_ids += [pas_token_id] * padding_length
        attn_mask += [0] * padding_length

    assert len(input_ids) == max_length

    return input_ids, attn_mask
