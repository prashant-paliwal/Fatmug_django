# Generated by Django 5.0 on 2023-12-09 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0002_purchaseorder_actual_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='po_number',
            field=models.CharField(editable=False, max_length=30, unique=True),
        ),
    ]
