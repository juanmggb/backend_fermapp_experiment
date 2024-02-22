from django.db import models
from django.core.validators import MinValueValidator
from experiment.models import Experiment

# Create your models here.


# It would be a good idea to allow users decide if they want to store the Analysis or not. Ig they want to store the analysis extra information would be required by the app
class Analysis(models.Model):
    #  If an Analysis can have multiple Experiments and an Experiment can belong to multiple Analyses, then a many-to-many relationship is appropriate.

    # SOMETHING SIMILAR WITH HAPPEND WITH EXPERIMENT AND MICROORGANISM, SUBSTRATES AND PRODUCTOS MantToMantField
    experiments = models.ManyToManyField(Experiment)
    date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=200)
    supervisor = models.CharField(max_length=200)
    # maybe i should consider operation and medium composition all as medium composition analysis
    analysis_type = models.CharField(
        max_length=200,
        choices=(
            ("kinetic parameters estimation", "kinetic parameters estimation"),
            # ("operation conditions optimization", "operation conditions optimization"),
            ("medium composition optimization", "medium composition optimization"),
        ),
    )

    observations = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.analysis_type}"


class AnalysisVariable(models.Model):
    analysis = models.ForeignKey(
        Analysis, on_delete=models.CASCADE, null=True, blank=True
    )

    variable_name = models.CharField(max_length=200)

    variable_units = models.CharField(max_length=200)

    variable_type = models.CharField(
        max_length=200, choices=(("discrete", "discrete"), ("continuous", "continuous"))
    )

    observations = models.TextField()

    def __str__(self):
        return f"{self.variable_name} - {self.variable_units}"


class AnalysisVariableValue(models.Model):
    variable = models.ForeignKey(
        AnalysisVariable, on_delete=models.CASCADE, blank=True, null=True
    )

    value = models.FloatField(validators=[MinValueValidator(0)])

    value_type = models.CharField(
        max_length=200,
        choices=(
            ("lower", "lower"),
            ("upper", "upper"),
            ("average", "average"),
            ("deviation", "deviation"),
            ("optimal", "optimal"),
        ),
    )

    def __str__(self):
        return f"{self.variable} - {self.value_type} - {self.value}"


class AnalysisKineticParameter(models.Model):
    analysis = models.ForeignKey(
        Analysis, on_delete=models.CASCADE, null=True, blank=True
    )

    parameter_name = models.CharField(max_length=200)

    parameter_units = models.CharField(max_length=200)

    observations = models.TextField()

    def __str__(self):
        return f"{self.parameter_name} - {self.parameter_units}"


class AnalysisKineticParameterValue(models.Model):
    parameter = models.ForeignKey(AnalysisKineticParameter, on_delete=models.CASCADE)

    value = models.FloatField(validators=[MinValueValidator(0)])

    value_type = models.CharField(
        max_length=200,
        choices=(
            ("lower", "lower"),
            ("upper", "upper"),
            ("average", "average"),
            ("deviation", "deviation"),
            ("optimal", "optimal"),
        ),
    )

    def __str__(self):
        return f"{self.parameter} - {self.value_type} - {self.value}"


# Low Agitation: Low agitation speeds are often employed during the initial stages of fermentation to ensure gentle mixing and prevent excessive shear stress on the microorganisms. Typical ranges for low agitation can be around 50-200 RPM.

# Moderate Agitation: As the fermentation progresses and the microorganisms multiply, moderate agitation is often applied to maintain proper mixing and prevent the formation of concentration gradients. Typical ranges for moderate agitation can be around 200-500 RPM.

# High Agitation: In certain fermentation processes, such as those involving high-density cultures or oxygen-demanding microorganisms, higher agitation speeds may be necessary to enhance mass transfer and oxygenation. High agitation speeds can range from 500-1000 RPM or even higher.


# Low Aeration: Low levels of aeration are often used during the initial stages of fermentation or for certain microorganisms that do not require high oxygen levels. Low aeration rates can range from 0.1 to 1 L/min or lower.

# Moderate Aeration: As the fermentation progresses and microbial growth increases, moderate levels of aeration may be necessary to maintain optimal oxygen levels for cell growth and metabolism. Moderate aeration rates can range from 1 to 10 L/min.

# High Aeration: Some fermentation processes, particularly those involving oxygen-demanding microorganisms or high-density cultures, require high levels of aeration to ensure sufficient oxygen supply. High aeration rates can range from 10 to 100 L/min or even higher.
