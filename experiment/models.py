from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from element.models import Substrate, Microorganism, Product
from users.models import Member, Laboratory

# Métodos de Modelo: Podrías considerar añadir métodos dentro de tus clases de modelo para operaciones comunes. Esto encapsula la lógica del modelo y facilita el mantenimiento del código.


# Experiment object
class Experiment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    # Author and Supervisor fields: If your app has a user system, consider changing the author and supervisor fields to a ForeignKey relationship with the User model instead of CharField.
    author = models.ForeignKey(
        Member, on_delete=models.SET_NULL, null=True, related_name="author_exp"
    )

    author_name = models.CharField(max_length=255, null=True)

    # It could be a good idea to register labs. So we might have a Laboratory Table
    laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True)

    laboratory_name = models.CharField(max_length=255, null=True)

    # For now, lets assume that an experiment contains only one microorganism, one substrate and one product

    # the blank=True is temporal
    substrate = models.ForeignKey(
        Substrate,
        on_delete=models.SET_NULL,
        null=True,
        related_name="substrate",
    )
    microorganism = models.ForeignKey(
        Microorganism,
        on_delete=models.SET_NULL,
        null=True,
        related_name="microorganism",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name="product",
    )

    # maybe i should consider operation and medium composition all as medium composition analysis
    experiment_type = models.CharField(
        max_length=200,
        choices=(
            ("kinetic", "kinetic"),
            # ("operation", "operation"),
            ("process optimization", "process optimization"),
        ),
    )

    observations = models.TextField(blank=True)

    #     Equipment Used: Information about the bioreactors, measuring devices, or any other specialized equipment used.

    # Standard Operating Procedure (SOP) ID: Reference to the SOP followed during the experiment, if applicable.

    # def __str__(self):
    #     return f"{self.date} - {self.microorganism.name} on {self.substrate.name} - {self.experiment_type}"


# ExperimentVariable contains the metadata associated with the experimental variable
# A single experiment can posses several variables

# Time Intervals: Specific time intervals at which samples were taken.

# Initial Conditions: Initial pH, temperature, etc.

# Sampling Method: Description of how the samples were collected.

# Analytical Methods: Methods used for measuring concentrations of biomass, substrate, and product.


# Design Type: Indication of the DOE method used (e.g., full factorial, fractional factorial, response surface methodology).

# Attachments: Option to attach supplementary files like images, lab notebook scans, or additional datasets.


# Growth Phase: Indication of the microbial growth phase during sampling (lag, exponential, stationary, death).
class ExperimentVariable(models.Model):
    # Estás usando ForeignKey correctamente, pero para mejor claridad, puedes añadir el atributo related_name para describir la relación en términos del modelo relacionado.
    experiment = models.ForeignKey(
        Experiment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="variables",
    )

    variable_name = models.CharField(max_length=200)

    variable_units = models.CharField(max_length=200)

    # variable_type = models.CharField(
    #     max_length=200, choices=(("discrete", "discrete"), ("continuous", "continuous"))
    # )

    detection_method = models.CharField(max_length=200, null=True, blank=True)

    # observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.variable_name} - {self.variable_units}"


# ExperimentVariableValue contains the actual set of values of the corresponding variable.
# A single variable can posses several values, so it is necessary to consider a table to sotre all those values associated with the corresponding variable
class ExperimentVariableValue(models.Model):
    variable = models.ForeignKey(
        ExperimentVariable,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="values",
    )

    value = models.FloatField(validators=[MinValueValidator(0)])

    # value_type = models.CharField(
    #     max_length=200, choices=(("measured", "measured"), ("literature", "literature"))
    # )

    def __str__(self):
        return f"{self.variable} - {self.value}"


class ExperimentKineticParameter(models.Model):
    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, null=True, blank=True
    )

    parameter_name = models.CharField(max_length=200)

    parameter_units = models.CharField(max_length=200)

    parameter_value = models.FloatField()

    observations = models.TextField()

    def __str__(self):
        return f"{self.parameter_name} - {self.parameter_units}"


# class ExperimentKineticParameterValue(models.Model):
#     parameter = models.ForeignKey(ExperimentKineticParameter, on_delete=models.CASCADE)

#     value = models.FloatField(validators=[MinValueValidator(0)])

#     value_type = models.CharField(
#         max_length=200, choices=(("measured", "measured"), ("literature", "literature"))
#     )

#     def __str__(self):
#         return f"{self.parameter} - {self.value_type} - {self.value}"


# Considerar restricciones en la optimizacion de medio de cultivo
# considerar analisis de varianza ANOVA


# Variable names:
# Culture medium
# cabon source, nitrogen source, mineral sales, growth factors, specific additives

# maybe i should consider operation and medium composition all as medium composition analysis
# Operation conditions
# temperature, pH, agitation, aeration,
# Concentration
# substrate, biomass, product

# ExperimentVariable and ExperimentKineticParameter: These two models seem to have very similar characteristics and might be combined into one model, depending on your needs. If they need to be kept separate, consider creating an abstract base class for them to reduce code repetition.
