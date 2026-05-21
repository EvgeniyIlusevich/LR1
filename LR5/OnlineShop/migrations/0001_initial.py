import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def primary_key():
    return models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')


FAQ_SCHEMA = [
    ('id', primary_key()),
    ('question', models.CharField(max_length=255)),
    ('answer', models.TextField()),
    ('date_added', models.DateTimeField(auto_now_add=True)),
]

PROMO_SCHEMA = [
    ('id', primary_key()),
    ('code', models.CharField(max_length=20, unique=True)),
    ('discount_percent', models.PositiveIntegerField(default=0, help_text='Discount percent')),
    ('active', models.BooleanField(default=True, help_text='Promo is active')),
]

EMPLOYEE_SCHEMA = [
    ('id', primary_key()),
    ('name', models.CharField(max_length=100)),
    ('photo', models.ImageField(default='images/default.jpg', upload_to='images/')),
    ('job_description', models.TextField()),
    ('phone', models.CharField(max_length=20)),
    ('email', models.EmailField(max_length=254)),
]

ARTICLE_SCHEMA = [
    ('id', primary_key()),
    ('title', models.CharField(max_length=200)),
    ('publication_date', models.DateField()),
    ('summary', models.TextField()),
    ('content', models.TextField(default='')),
    ('author', models.CharField(max_length=100)),
    ('image', models.ImageField(default='images/default.jpg', upload_to='images/')),
]

CUSTOMER_SCHEMA = [
    ('id', primary_key()),
    ('first_name', models.CharField(max_length=50)),
    ('last_name', models.CharField(max_length=50)),
    ('email', models.EmailField(max_length=254, unique=True)),
    ('phone', models.CharField(max_length=15)),
]

PRODUCT_SCHEMA = [
    ('id', primary_key()),
    ('name', models.CharField(max_length=100)),
    ('price', models.DecimalField(decimal_places=2, max_digits=10)),
    ('unit', models.CharField(choices=[('pcs', 'Штуки'), ('kg', 'Килограммы'), ('l', 'Литры')], default='pcs', max_length=3)),
]

ADDRESS_SCHEMA = [
    ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='OnlineShop.customer')),
    ('address_line_1', models.CharField(max_length=255)),
    ('address_line_2', models.CharField(blank=True, max_length=255, null=True)),
    ('city', models.CharField(max_length=100)),
    ('state', models.CharField(max_length=100)),
    ('postal_code', models.CharField(max_length=20)),
    ('country', models.CharField(max_length=100)),
]

SALE_SCHEMA = [
    ('id', primary_key()),
    ('sale_date', models.DateTimeField(auto_now_add=True)),
    ('delivery_date', models.DateTimeField()),
    ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
    ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineShop.customer')),
]

SALE_PRODUCT_SCHEMA = [
    ('id', primary_key()),
    ('quantity', models.PositiveIntegerField()),
    ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
    ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineShop.product')),
    ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OnlineShop.sale')),
]

REVIEW_SCHEMA = [
    ('id', primary_key()),
    ('text', models.TextField()),
    ('rating', models.PositiveSmallIntegerField(default=1)),
    ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
    ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='OnlineShop.product')),
]


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(name='FAQ', fields=FAQ_SCHEMA),
        migrations.CreateModel(name='PromoCode', fields=PROMO_SCHEMA),
        migrations.CreateModel(name='Employee', fields=EMPLOYEE_SCHEMA),
        migrations.CreateModel(name='Article', fields=ARTICLE_SCHEMA),
        migrations.CreateModel(name='Customer', fields=CUSTOMER_SCHEMA),
        migrations.CreateModel(name='Product', fields=PRODUCT_SCHEMA),
        migrations.CreateModel(name='CustomerAddress', fields=ADDRESS_SCHEMA),
        migrations.CreateModel(name='Sale', fields=SALE_SCHEMA),
        migrations.CreateModel(name='SaleProduct', fields=SALE_PRODUCT_SCHEMA),
        migrations.CreateModel(name='Review', fields=REVIEW_SCHEMA),
        migrations.AddField(
            model_name='sale',
            name='products',
            field=models.ManyToManyField(through='OnlineShop.SaleProduct', to='OnlineShop.product'),
        ),
    ]