# Generated by Django 4.2.3 on 2023-10-14 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_laboratory_alter_member_role_member_laboratory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='laboratory',
            options={'verbose_name_plural': 'Laboratories'},
        ),
        migrations.AddField(
            model_name='laboratory',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='laboratory',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='laboratory',
            name='director',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_laboratory', to='users.member'),
        ),
        migrations.AddField(
            model_name='laboratory',
            name='email',
            field=models.EmailField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='laboratory',
            name='location',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='laboratory',
            name='phone_number',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='laboratory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lab_director', to='users.laboratory'),
        ),
    ]
