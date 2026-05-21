import django.db.models.deletion
from django.db import migrations, models


def default_id():
    return models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')


CATEGORY_FIELDS = [
    ('id', default_id()),
    ('name', models.CharField(max_length=100)),
]

UNIT_CHOICES = [
    ('pcs', 'Штук'),
    ('kg', 'Килограммы'),
    ('l', 'Литры'),
]


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineShop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=CATEGORY_FIELDS,
        ),
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(choices=UNIT_CHOICES, default='pcs', max_length=3),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='products',
                to='OnlineShop.category',
            ),
        ),
    ]