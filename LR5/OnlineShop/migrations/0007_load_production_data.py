import os
from django.db import migrations
from django.core.management import call_command
from django.conf import settings

def load_fixture(apps, schema_editor):
    fixture_path = os.path.join(settings.BASE_DIR, 'OnlineShop', 'fixtures', 'data_new.json')
    if os.path.exists(fixture_path):
        call_command('loaddata', fixture_path)
        print(f"✅ Данные загружены из {fixture_path}")
    else:
        print(f"⚠️ Файл {fixture_path} не найден, данные не загружены.")

def unload_fixture(apps, schema_editor):
    # Откат не нужен
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('OnlineShop', '0006_remove_customer_city_sale_city'),  # Укажите последнюю существующую миграцию
    ]

    operations = [
        migrations.RunPython(load_fixture, unload_fixture),
    ]