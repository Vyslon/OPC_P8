# Generated by Django 2.1.5 on 2019-03-19 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Substitute_Platform', '0013_auto_20190306_0938'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='platform_user',
            unique_together={('substituted_product', 'substituent_product')},
        ),
    ]
