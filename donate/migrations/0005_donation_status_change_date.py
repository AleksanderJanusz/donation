# Generated by Django 4.2.2 on 2023-07-07 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donate', '0004_donation_is_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='status_change_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
