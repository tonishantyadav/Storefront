# Generated by Django 4.2.2 on 2023-06-23 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_rename_feature_product_collection_featured_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Collection',
            new_name='collection',
        ),
    ]
