# Generated by Django 4.2.2 on 2023-07-07 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donate', '0005_donation_status_change_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='status_change_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
