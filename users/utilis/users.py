from django.utils.dateparse import parse_date
from datetime import timedelta


# Create a function to handle date filtering
def filter_by_date(queryset, initialdate, finaldate):
    if initialdate:
        initialdate = parse_date(initialdate)
    if finaldate:
        finaldate = parse_date(finaldate)

    if initialdate and finaldate:
        # Correct usage of range for filtering between two dates
        return queryset.filter(created_at__range=[initialdate, finaldate])

    elif initialdate:
        # Filter from initialdate to an open-ended future
        return queryset.filter(created_at__gte=initialdate)

    elif finaldate:
        # Filter up to and including finaldate
        return queryset.filter(created_at__lte=finaldate)

    return queryset


filter_dict = {
    "name": "laboratory_name",
    "location": "location",
    "director": "director_name",
    "recent_first": "-created_at",
    "recent_last": "created_at",
}

filter_dict_member = {
    "name": "name",
    "laboratory": "laboratory_name",
    "role": "role",
    "recent_first": "-created_at",
    "recent_last": "created_at",
}
