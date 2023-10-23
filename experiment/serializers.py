from rest_framework import serializers
from .models import Experiment, ExperimentVariable, ExperimentVariableValue


class ExperimentVariableValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentVariableValue
        fields = "__all__"


class ExperimentVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentVariable
        fields = "__all__"


class ReducedExperimentVariableSerializer(serializers.ModelSerializer):
    values_list = serializers.SerializerMethodField()

    class Meta:
        model = ExperimentVariable
        fields = ("variable_name", "variable_units", "detection_method", "values_list")

    def get_values_list(self, obj):
        # Fetch only the 'value' field from the related ExperimentVariableValue objects
        values = obj.values.values_list("value", flat=True)

        # Convert QuerySet to Python list
        value_list = list(values)

        # Return the list
        return value_list


class ExperimentSerializer(serializers.ModelSerializer):
    variables = ReducedExperimentVariableSerializer(read_only=True, many=True)

    # Always rememeber to use read_only with serializer fields that DON'T exist in the model
    substrate = serializers.CharField(source="substrate.name", read_only=True)
    microorganism = serializers.CharField(source="microorganism.name", read_only=True)
    product = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Experiment
        fields = "__all__"
