# Generated by Django 4.2.3 on 2023-11-04 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0009_alter_experiment_microorganism_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='supervisor',
        ),
    ]
