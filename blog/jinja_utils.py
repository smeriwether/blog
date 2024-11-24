from datetime import datetime

import pytz
from markupsafe import Markup

from blog.utils import sanitize_html


def safe_html(text):
    return Markup(sanitize_html(text))


def relative_datetime(value, include_relative=True):
    eastern = pytz.timezone("US/Eastern")
    if value.tzinfo is None:
        value = pytz.utc.localize(value)
    eastern_dt = value.astimezone(eastern)

    # Get current time in Eastern
    now = datetime.now(eastern)

    # Calculate time difference
    diff = now - eastern_dt

    if include_relative:
        if diff.days == 0:
            if diff.seconds < 60:
                return "just now"
            if diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
            if diff.seconds < 86400:
                hours = diff.seconds // 3600
                return f'{hours} hour{"s" if hours != 1 else ""} ago'
        if diff.days == 1:
            return "Yesterday"
        if diff.days < 7:
            return f"{diff.days} days ago"

    # Fall back to regular format for older dates
    return eastern_dt.strftime("%B %d, %Y %I:%M %p %Z")
