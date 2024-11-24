import bleach
from bleach.css_sanitizer import CSSSanitizer


def sanitize_html(html_content):
    # Define allowed tags
    allowed_tags = [
        "p",
        "br",
        "strong",
        "em",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "ul",
        "ol",
        "li",
        "a",
        "img",
        "blockquote",
        "pre",
        "code",
    ]

    # Define allowed attributes
    allowed_attrs = {
        "*": ["class"],
        "a": ["href", "title"],
        "img": ["src", "alt", "title"],
    }

    # Define allowed CSS properties
    css_sanitizer = CSSSanitizer(
        allowed_css_properties=["color", "background-color", "text-align"]
    )

    # Clean the HTML
    clean_html = bleach.clean(
        html_content,
        tags=allowed_tags,
        attributes=allowed_attrs,
        css_sanitizer=css_sanitizer,
        strip=True,
    )

    return clean_html
