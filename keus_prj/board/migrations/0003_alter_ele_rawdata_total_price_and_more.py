# Generated by Django 4.2.7 on 2023-12-06 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_alter_ele_rawdata_citizen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ele_rawdata',
            name='total_price',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ele_rawdata',
            name='total_use',
            field=models.CharField(max_length=255),
        ),
    ]
