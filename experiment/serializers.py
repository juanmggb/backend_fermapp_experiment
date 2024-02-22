from rest_framework import serializers
from .models import Experiment, ExperimentVariable, ExperimentVariableValue


class ExperimentVariableValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentVariableValue
        fields = "__all__"


# class ExperimentVariableSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExperimentVariable
#         fields = "__all__"


class ExperimentVariableSerializer(serializers.ModelSerializer):
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
    # Note: It's important to use read_only fields for attributes that don't exist in the model
    variables = ExperimentVariableSerializer(many=True, read_only=True)
    substrate_name = serializers.CharField(source="substrate.name", read_only=True)
    microorganism_name = serializers.CharField(
        source="microorganism.name", read_only=True
    )
    product_name = serializers.CharField(source="product.name", read_only=True)
    author_name = serializers.CharField(source="author.name", read_only=True)
    laboratory_name = serializers.CharField(
        source="laboratory.laboratory_name", read_only=True
    )

    class Meta:
        model = Experiment
        fields = "__all__"
        # write_only_fields is deprecated in DRF 3.x; use 'extra_kwargs' instead
        # extra_kwargs = {
        #     "substrate": {"write_only": True},
        #     "product": {"write_only": True},
        #     "microorganism": {"write_only": True},
        #     "author": {"write_only": True},
        #     "supervisor": {"write_only": True},
        #     "laboratory": {"write_only": True},
        # }
