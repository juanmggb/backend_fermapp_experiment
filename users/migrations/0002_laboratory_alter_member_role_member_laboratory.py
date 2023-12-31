# Generated by Django 4.2.3 on 2023-10-14 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('laboratory_name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.CharField(choices=[('Lab Director', 'Lab Director'), ('Student Researcher', 'Student Researcher')], default='Student Researcher', max_length=200),
        ),
        migrations.AddField(
            model_name='member',
            name='laboratory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.laboratory'),
        ),
    ]
