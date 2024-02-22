from django.contrib import admin
from analysis.models import (
    Analysis,
    AnalysisVariable,
    AnalysisVariableValue,
    AnalysisKineticParameter,
    AnalysisKineticParameterValue,
)

# Register your models here.


admin.site.register(Analysis)
admin.site.register(AnalysisVariable)
admin.site.register(AnalysisVariableValue)
admin.site.register(AnalysisKineticParameter)
admin.site.register(AnalysisKineticParameterValue)
