

from .models import Experiment, ExperimentVariable, ExperimentVariableValue
from experiment.serializers import ExperimentSerializer, ExperimentVariableSerializer, ExperimentVariableValueSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class ExperimentViewSet(ModelViewSet):

    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer 


class ExperimentVariableViewSet(ModelViewSet):

    queryset = ExperimentVariable.objects.all()
    serializer_class = ExperimentVariableSerializer


class ExperimentVariableValueViewSet(ModelViewSet):

    queryset = ExperimentVariableValue.objects.all()
    serializer_class = ExperimentVariableValueSerializer 
class CreateExperimentObjects(APIView):
    def post(self, request):
        experiment_data = request.data.get('experiment')
        variables_data = request.data.get('variables')

        experiment_serializer = ExperimentSerializer(data=experiment_data)
        variable_serializer = ExperimentVariableSerializer(data=variables_data, many=True)

        if experiment_serializer.is_valid() and variable_serializer.is_valid():
            experiment = experiment_serializer.save()

            variables = variable_serializer.save(experiment=experiment)
            for variable, variable_data in zip(variables, variables_data):
                values_data = variable_data.pop('values')

                for value_data in values_data:
                    value_data['variable'] = variable.id
                    value_serializer = ExperimentVariableValueSerializer(data=value_data)

                    if value_serializer.is_valid(raise_exception=True):
                        value_serializer.save()

            return Response(experiment_serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {
                'errors': {
                    'experiment': experiment_serializer.errors if experiment_serializer.errors else None,
                    'variables': variable_serializer.errors if variable_serializer.errors else None,
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )
