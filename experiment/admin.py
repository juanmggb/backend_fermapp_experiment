from django.contrib import admin

from element.models import Substrate, Microorganism, Product
from experiment.models import Experiment, ExperimentVariable, ExperimentVariableValue
# Register your models here.


admin.site.register(Substrate)
admin.site.register(Microorganism)
admin.site.register(Product)

admin.site.register(Experiment)
admin.site.register(ExperimentVariable)
admin.site.register(ExperimentVariableValue)
