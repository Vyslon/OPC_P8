# Generated by Django 2.1.5 on 2019-02-25 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Substitute_Platform', '0007_auto_20190225_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform_user',
            name='substituted_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produit_substite', to='Substitute_Platform.Products'),
        ),
    ]
