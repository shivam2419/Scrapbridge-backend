# Generated by Django 5.0.4 on 2025-03-30 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0010_payments_transaction_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payments',
            options={'ordering': ['-created']},
        ),
    ]
