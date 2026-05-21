from django.db import migrations, models


def set_category_not_null(apps, schema_editor):
    product_model = apps.get_model('OnlineShop', 'Product')
    category_model = apps.get_model('OnlineShop', 'Category')
    
    default_category = category_model.objects.first()
    product_model.objects.filter(category__isnull=True).update(category=default_category)


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineShop', '0002_category_alter_product_unit_product_category'),
    ]

    operations = [
        migrations.RunPython(set_category_not_null),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name='products',
                to='OnlineShop.category',
            ),
        ),
    ]