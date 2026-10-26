from django import template

register = template.Library()


@register.filter
def playtime(value):
    try:
        minutes = int(value or 0)
    except (TypeError, ValueError):
        return "0 min"

    minutes = max(minutes, 0)
    hours, remaining_minutes = divmod(minutes, 60)

    parts = []

    if hours:
        unit = "hr" if hours == 1 else "hrs"
        parts.append(f"{hours} {unit}")

    if remaining_minutes or not parts:
        parts.append(f"{remaining_minutes} min")

    return " ".join(parts)
