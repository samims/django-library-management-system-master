# Generated by Django 2.2 on 2019-06-10 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_auto_20190610_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]