import textwrap

def wrapText(text, width):
    out = []
    for line in text.splitlines():
        if line.strip() != '':
            out.extend(textwrap.wrap(line, width, break_long_words=False, replace_whitespace=False))
    return out
