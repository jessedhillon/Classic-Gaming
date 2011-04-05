import re

def slugify(text, separator="-"):
    slug = ""
    for c in text.lower():
        slug += c

    slug = re.sub("([a-zA-Z])(uml|acute|grave|circ|tilde|cedil)", r"\1", slug)
    slug = re.sub("\W", " ", slug)
    slug = re.sub(" +", separator, slug)

    return slug.strip()
