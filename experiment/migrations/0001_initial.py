# Generated by Django 4.2.3 on 2024-02-22 18:22

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '__first__'),
        ('element', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('experiment_type', models.CharField(choices=[('kinetic', 'kinetic'), ('process optimization', 'process optimization')], max_length=200)),
                ('observations', models.TextField(blank=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_exp', to=settings.AUTH_USER_MODEL)),
                ('laboratory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lab_experiments', to='users.laboratory')),
                ('microorganism', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='microorganism', to='element.microorganism')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='element.product')),
                ('substrate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='substrate', to='element.substrate')),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentVariable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable_name', models.CharField(max_length=200)),
                ('variable_units', models.CharField(max_length=200)),
                ('detection_method', models.CharField(blank=True, max_length=200, null=True)),
                ('experiment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variables', to='experiment.experiment')),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentVariableValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('variable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='values', to='experiment.experimentvariable')),
            ],
        ),
    ]
