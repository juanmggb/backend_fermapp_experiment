from rest_framework.response import Response
from experiment.models import Experiment, ExperimentVariable, ExperimentVariableValue
from experiment.serializers import ExperimentSerializer
from rest_framework.decorators import api_view
from django.db import transaction


@api_view(["GET", "POST"])
@transaction.atomic  # Add this line to make the function transactional
def experiment_list(request):
    if request.method == "GET":
        experiments = Experiment.objects.all().order_by("-id")

        serializer = ExperimentSerializer(experiments, many=True)

        return Response(serializer.data, status=200)

    elif request.method == "POST":
        data = request.data
        experiment_details = data.get("experimentDetails")

        # Throw an error if experimentDetails are not provided
        if not experiment_details:
            return Response({"error": "experimentDetails is required"}, status=400)

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

                print("VALUES", values)

                if len(values) == 0:
                    return Response(
                        {"error": "all variables required values"}, status=400
                    )
                for value in values:
                    ExperimentVariableValue.objects.create(
                        variable=experiment_variable,
                        value=value,
                    )

            return Response(serializer.data, status=200)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)


# By adding the @transaction.atomic decorator above the create_experiment function, you're telling Django to treat all the database operations in this function as a single transaction. This means if any of the operations fail, all changes to the database within this function will be rolled back, leaving your database in a consistent state.
