# Generated by Django 2.1.5 on 2019-03-06 09:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Substitute_Platform', '0012_auto_20190228_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform_user',
            name='substituent_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produit_substituant', to='Substitute_Platform.Products'),
        ),
        migrations.AlterField(
            model_name='platform_user',
            name='substituted_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='produit_substitute', to='Substitute_Platform.Products'),
        ),
        migrations.AlterField(
            model_name='platform_user',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
