# Source - https://stackoverflow.com/a
# Posted by Rishav Shahil, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-28, License - CC BY-SA 4.0

from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def timesince_single_unit(value):
    """
    Custom timesince filter to show only the first unit (like '18 hr' or '16 min').
    """
    if not value:
        return ""
    
    # Get the full timesince output (e.g., "18 hours, 16 minutes")
    time_str = timesince(value)
    
    # Split by the comma and keep only the first unit
    first_unit = time_str.split(",")[0]
    
    # Optionally, abbreviate 'hours' to 'hr' and 'minutes' to 'min'
    first_unit = first_unit.replace("hours", "hrs").replace("minutes", "mins")
    first_unit = first_unit.replace("hour", "hr").replace("minute", "min")

    return first_unit
