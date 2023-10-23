# Generated by Django 4.2.3 on 2023-10-14 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_laboratory_director'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratory',
            name='director',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_laboratory', to='users.member'),
        ),
        migrations.AlterField(
            model_name='member',
            name='laboratory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lab_director', to='users.laboratory'),
        ),
    ]