# Generated by Django 3.0.8 on 2020-07-10 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbtest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
