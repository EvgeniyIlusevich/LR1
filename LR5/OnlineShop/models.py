from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from decimal import Decimal
from datetime import date


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ('pcs', 'Штук'),
        ('kg', 'Килограммы'),
        ('l', 'Литры'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    unit = models.CharField(max_length=3, choices=UNIT_CHOICES, default='pcs')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def clean(self):
        if self.price <= 0:
            raise ValidationError({'price': 'Цена товара должна быть больше нуля.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({'rating': 'Рейтинг должен быть от 1 до 5.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Review for {self.product.name} by {self.author.username}'


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+375\d{9}$', message='Телефон должен быть в формате +375XXXXXXXXX')]
    )

    def clean(self):
        if not self.email:
            raise ValidationError({'email': 'Email обязателен.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='SaleProduct')
    sale_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    city = models.CharField(max_length=100, default="Неизвестно")

    def clean(self):
        if self.delivery_date and self.sale_date and self.delivery_date < self.sale_date:
            raise ValidationError({'delivery_date': 'Дата доставки не может быть раньше даты продажи.'})
        if self.total_price is not None and self.total_price < 0:
            raise ValidationError({'total_price': 'Общая цена не может быть отрицательной.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale {self.id} to {self.customer}"


class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'Количество товара должно быть положительным.'})
        if self.price < 0:
            raise ValidationError({'price': 'Цена не может быть отрицательной.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"SaleProduct {self.id}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField()
    summary = models.TextField()
    content = models.TextField(default='')
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', default='images/default.jpg')

    def clean(self):
        if self.publication_date and self.publication_date > date.today():
            raise ValidationError({'publication_date': 'Дата публикации не может быть в будущем.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.question or not self.answer:
            raise ValidationError('Вопрос и ответ не могут быть пустыми.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question


class Employee(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/', default='images/default.jpg')
    job_description = models.TextField()
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^\+375\d{9}$', message='Телефон должен быть в формате +375XXXXXXXXX')]
    )
    email = models.EmailField()

    def clean(self):
        if not self.name:
            raise ValidationError({'name': 'Имя сотрудника обязательно.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField(
        default=0,
        help_text="Discount percent",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    active = models.BooleanField(default=True, help_text="Promo is active")

    def clean(self):
        if self.discount_percent < 0 or self.discount_percent > 100:
            raise ValidationError({'discount_percent': 'Процент скидки должен быть от 0 до 100.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    published_date = models.DateField(auto_now_add=True)

    def clean(self):
        if self.salary is not None and self.salary < 0:
            raise ValidationError({'salary': 'Зарплата не может быть отрицательной.'})
        if not self.title:
            raise ValidationError({'title': 'Название вакансии обязательно.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title