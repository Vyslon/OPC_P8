# Generated by Django 2.1.5 on 2019-02-11 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Substitute_Platform', '0004_remove_products_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platform_user',
            name='substituent_product',
        ),
        migrations.AddField(
            model_name='platform_user',
            name='substituent_product',
            field=models.ManyToManyField(related_name='produit_substituant', to='Substitute_Platform.Products'),
        ),
        migrations.RemoveField(
            model_name='platform_user',
            name='substituted_product',
        ),
        migrations.AddField(
            model_name='platform_user',
            name='substituted_product',
            field=models.ManyToManyField(related_name='produit_substite', to='Substitute_Platform.Products'),
        ),
    ]
