# Generated by Django 4.2.3 on 2023-11-12 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_member_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='laboratory_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]