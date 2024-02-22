from rest_framework.response import Response
from experiment.models import Experiment, ExperimentVariable, ExperimentVariableValue
from experiment.serializers import ExperimentSerializer
from rest_framework.decorators import api_view
from django.db import transaction
from django.db.models import Q
from .utilis.experiments import filter_by_date, filter_dict


@api_view(["GET", "POST"])
@transaction.atomic  # Add this line to make the function transactional
def experiment_list(request):
    if request.method == "GET":
        # Get filter params from request

        filterby = request.GET.get("filterby", "")
        search = request.GET.get("search", "")
        sortby = request.GET.get("sortby", "")
        initialdate = request.GET.get("initialdate", "")
        finaldate = request.GET.get("finaldate", "")

        filters = Q()
        if filterby and search:
            filters = Q(**{f"{filter_dict[filterby]}__icontains": search})

        queryset = Experiment.objects.filter(filters)

        queryset = filter_by_date(queryset, initialdate, finaldate)

        # filter_dict = {
        #     "author": "author_name",
        #     "laboratory": "laboratory_name",
        #     "experiment_type": "experiment_type",
        #     "recent_first": "-date",
        #     "recent_last": "date",
        # }

        queryset = queryset.order_by(filter_dict.get(sortby, "-id"))

        # Pagination here
        # experiments = Experiment.objects.all().order_by("-id")

        serializer = ExperimentSerializer(queryset, many=True)

        return Response(serializer.data, status=200)

    elif request.method == "POST":
        data = request.data

        experiment_details = data.get("experimentDetails")

        # Throw an error if experimentDetails are not provided
        if not experiment_details:
            return Response({"error": "experiment details are required"}, status=400)

        serializer = ExperimentSerializer(
            data=experiment_details
        )  # Pass data to serializer

        if serializer.is_valid():
            experiment = serializer.save()
            variables = data.get("variables")

            # Throw an error if variables are not provided
            if not variables:
                return Response({"error": "variables are required"}, status=400)

            for variable in variables:
                experiment_variable = ExperimentVariable.objects.create(
                    experiment=experiment,
                    variable_name=variable.get("variable_name"),
                    variable_units=variable.get("variable_units"),
                    detection_method=variable.get("detection_method"),
                )

                values = variable.get("values", [])


                if len(values) == 0:
                    return Response(
                        {"error": "all variables require values"}, status=400
                    )
                for value in values:
                    ExperimentVariableValue.objects.create(
                        variable=experiment_variable,
                        value=value,
                    )

            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)


# By adding the @transaction.atomic decorator above the create_experiment function, you're telling Django to treat all the database operations in this function as a single transaction. This means if any of the operations fail, all changes to the database within this function will be rolled back, leaving your database in a consistent state.


@api_view(["GET", "PUT", "DELETE"])
def experiment_details(request, id):
    try:
        experiment = Experiment.objects.get(id=id)
    except Experiment.DoesNotExist:
        return Response(
            {"message": "Experiment with given id doesn't exist"}, status=404
        )

    if request.method == "GET":
        serializer = ExperimentSerializer(experiment)
        return Response(serializer.data, status=200)

    elif request.method == "PUT":
        serializer = ExperimentSerializer(data=request.data, instance=experiment)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)
        print(serializer.errors)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        experiment.delete()

        return Response({"message": "Experiment deleted successfully"}, status=200)
