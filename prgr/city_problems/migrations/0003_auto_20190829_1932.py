# Generated by Django 2.2.4 on 2019-08-29 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('city_problems', '0002_auto_20190829_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='city_problems.Status'),
        ),
    ]
