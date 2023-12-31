# Generated by Django 4.2.3 on 2023-10-12 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('element', '0001_initial'),
        ('experiment', '0004_remove_experimentvariable_observations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='microorganism',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='element.microorganism'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='element.product'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='substrate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='element.substrate'),
        ),
    ]
