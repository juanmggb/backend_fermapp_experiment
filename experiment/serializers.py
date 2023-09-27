from rest_framework import serializers
from .models import Experiment, ExperimentVariable, ExperimentVariableValue

class ExperimentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experiment
        fields = '__all__'


class ExperimentVariableSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExperimentVariable
        fields = '__all__'



class ExperimentVariableValueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExperimentVariableValue
        fields = '__all__'
