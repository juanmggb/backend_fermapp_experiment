from django.utils.dateparse import parse_date
from datetime import timedelta


# Create a function to handle date filtering
def filter_by_date(queryset, initialdate, finaldate):
    if initialdate:
        initialdate = parse_date(initialdate)
    if finaldate:
        finaldate = parse_date(finaldate)

    if initialdate and finaldate:
        return queryset.filter(date__date__range=[initialdate, finaldate])

    elif initialdate:
        return queryset.filter(date__date__gte=initialdate)

    elif finaldate:
        return queryset.filter(date__date__lte=finaldate)

    return queryset


filter_dict = {
    "author": "author_name",
    "laboratory": "laboratory_name",
    "experiment_type": "experiment_type",
    "recent_first": "-date",
    "recent_last": "date",
}
