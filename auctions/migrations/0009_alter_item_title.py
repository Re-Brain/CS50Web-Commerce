# Generated by Django 4.2.3 on 2023-08-05 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_item_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.TextField(default=''),
        ),
    ]
