# Generated by Django 3.1.5 on 2021-06-24 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electoralroll', '0009_voter_anubhag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='anubhag',
            field=models.CharField(blank=True, default='-', max_length=100, null=True),
        ),
    ]
