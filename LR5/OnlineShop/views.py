import json
from decimal import Decimal
from statistics import mean, median, mode, StatisticsError
import io

import requests
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CustomUserCreationForm, ProductEdit, SaleProductForm, ReviewForm
from .models import Product, Customer, Sale, SaleProduct, Article, FAQ, Employee, Review, PromoCode, Category, Vacancy


def get_random_gif():
    api_key = 'Eio5GQwmcuMOFpcd811Iu4fvlUBVjVDN'
    url = f'https://api.giphy.com/v1/gifs/random?api_key={api_key}&rating=g'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('data', {}).get('images', {}).get('original', {}).get('url')
    except (requests.exceptions.RequestException, ValueError, TypeError) as e:
        print(f"Giphy API error: {e}")
        return None


def get_random_joke():
    url = 'https://official-joke-api.appspot.com/random_joke'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return f"{data.get('setup')} - {data.get('punchline')}"
    except (requests.exceptions.RequestException, ValueError, TypeError) as e:
        print(f"Joke API error: {e}")
        return None


def product_list(request):
    products = Product.objects.all()
    
    filters = {}
    if min_price := request.GET.get('min_price'):
        filters['price__gte'] = min_price
    if max_price := request.GET.get('max_price'):
        filters['price__lte'] = max_price
    if category_id := request.GET.get('category'):
        filters['category_id'] = category_id

    if filters:
        products = products.filter(**filters)

    categories = Category.objects.all()
    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
    })


def create_product(request):
    form = ProductEdit(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        Product.objects.create(**form.cleaned_data)
        return redirect('products_list')
    
    return render(request, 'create_product.html', {'form': form})


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    form = ProductEdit(request.POST or None, initial={
        'name': product.name,
        'price': product.price,
        'unit': product.unit,
        'category': product.category
    })
    
    if request.method == "POST" and form.is_valid():
        for field, value in form.cleaned_data.items():
            setattr(product, field, value)
        product.save()
        return redirect('products_list')
        
    return render(request, 'edit_product.html', {'form': form, 'product': product})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('products_list')
    return None


@transaction.atomic
def buy_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = SaleProductForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        promo_code = form.cleaned_data.get('promo_code')
        discount = Decimal('0.00')

        if promo_code:
            promo = PromoCode.objects.filter(code=promo_code, active=True).first()
            if not promo:
                form.add_error('promo_code', 'Промокод недействителен или неактивен')
                return render(request, 'buy_product.html', {'form': form, 'product': product})
            discount = Decimal(promo.discount_percent) / Decimal(100)

        customer = get_object_or_404(Customer, email=request.user.email)
        quantity = form.cleaned_data['quantity']
        price_with_discount = round(product.price * (Decimal('1.00') - discount), 2)
        total_price = round(price_with_discount * quantity, 2)

        sale = Sale.objects.create(
            city=form.cleaned_data.get('city'),
            customer=customer,
            delivery_date=timezone.now() + timezone.timedelta(days=7),
            total_price=total_price
        )

        SaleProduct.objects.create(
            sale=sale,
            product=product,
            quantity=quantity,
            price=price_with_discount
        )
        return redirect('products_list')

    return render(request, 'buy_product.html', {'form': form, 'product': product})


@staff_member_required
def sale_list(request):
    selected_city = request.GET.get('city')
    sales = Sale.objects.select_related('customer').prefetch_related('saleproduct_set__product')
    
    if selected_city:
        sales = sales.filter(city=selected_city)

    unique_cities = Sale.objects.values_list('city', flat=True).distinct().order_by('city')

    customers = Customer.objects.annotate(
        total_spent=Sum(F('sale__saleproduct__quantity') * F('sale__saleproduct__price'))
    ).order_by('last_name', 'first_name')

    sales_total_by_customer = {
        f"{c.first_name} {c.last_name}": round(c.total_spent or 0, 2)
        for c in customers
    }

    sales_totals = list(sales_total_by_customer.values())
    sales_mean = sales_median = 0
    sales_mode = "Нет моды"
    
    if sales_totals:
        sales_mean = round(mean(sales_totals), 2)
        sales_median = round(median(sales_totals), 2)
        try:
            sales_mode = round(mode(sales_totals), 2)
        except StatisticsError:
            pass

    product_sales = SaleProduct.objects.values('product__category__name').annotate(
        total_quantity=Sum('quantity'),
        total_profit=Sum(F('quantity') * F('product__price'))
    )

    most_pop = product_sales.order_by('-total_quantity').first()
    most_popular_type = most_pop['product__category__name'] if most_pop else "Нет данных"

    most_prof = product_sales.order_by('-total_profit').first()
    most_profitable_type = most_prof['product__category__name'] if most_prof else "Нет данных"

    most_demanded = SaleProduct.objects.values('product__name').annotate(
        total=Sum('quantity')
    ).order_by('-total').first()
    most_demanded_product_name = most_demanded['product__name'] if most_demanded else "Нет данных"

    sold_product_ids = SaleProduct.objects.values_list('product_id', flat=True).distinct()
    unsold_products = Product.objects.exclude(id__in=sold_product_ids)

    monthly_sales = SaleProduct.objects.annotate(
        month=TruncMonth('sale__sale_date')
    ).values('month', 'product__category__name').annotate(
        total=Sum('quantity')
    ).order_by('month')

    return render(request, 'sale_list.html', {
        'sales': sales,
        'unique_cities': unique_cities,
        'selected_city': selected_city,
        'sales_total_by_customer': sales_total_by_customer,
        'sales_mean': sales_mean,
        'sales_median': sales_median,
        'sales_mode': sales_mode,
        'most_popular_type': most_popular_type,
        'most_profitable_type': most_profitable_type,
        'most_demanded_product_name': most_demanded_product_name,
        'unsold_products': unsold_products,
        'monthly_sales': monthly_sales,
    })


@staff_member_required
def sales_chart(request):
    selected_city = request.GET.get('city', '')
    qs = SaleProduct.objects.all()
    if selected_city:
        qs = qs.filter(sale__city=selected_city)

    monthly_sales = qs.annotate(
        month=TruncMonth('sale__sale_date')
    ).values('month').annotate(
        total=Sum('quantity')
    ).order_by('month')

    months = []
    totals = []
    for item in monthly_sales:
        months.append(item['month'].strftime('%Y-%m'))
        totals.append(float(item['total']))

    if not months:
        months = ['Нет данных']
        totals = [0]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(months, totals, marker='o', linestyle='-', color='#6366f1', linewidth=2, markersize=6)
    ax.fill_between(months, totals, alpha=0.2, color='#6366f1')
    ax.set_title('Динамика продаж по месяцам', fontsize=14)
    ax.set_xlabel('Месяц', fontsize=12)
    ax.set_ylabel('Количество проданных единиц', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return HttpResponse(buf, content_type='image/png')


def latest_article(request):
    latest_article_obj = Article.objects.latest('publication_date')
    return render(request, 'latest_article.html', {'article': latest_article_obj, 'user': request.user})


def about_us(request):
    return render(request, 'about_us.html', {'user': request.user})


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles, 'user': request.user})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_detail.html', {'article': article})


def faq_list(request):
    faqs = FAQ.objects.all().order_by('-date_added')
    return render(request, 'faq_list.html', {'faqs': faqs, 'user': request.user})


def contact_list(request):
    employees = Employee.objects.all()
    return render(request, 'contact_list.html', {'employees': employees, 'user': request.user})


@transaction.atomic
def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        Customer.objects.get_or_create(
            email=user.email,
            defaults={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': form.cleaned_data.get('phone')
            }
        )
        login(request, user)
        return redirect('about_us')
        
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            username=form.cleaned_data.get('username'), 
            password=form.cleaned_data.get('password')
        )
        if user is not None:
            login(request, user)
            return redirect('about_us')
            
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def main_info(request):
    return render(request, 'jokes.html', {'random_joke': get_random_joke()})


def privacy_policy_page(request):
    return render(request, "gif.html", {"random_gif_url": get_random_gif()})


def product_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all() 
    
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.author = request.user
        review.save()
        return redirect('product_reviews', product_id=product_id)

    return render(request, 'product_reviews.html', {
        'product': product,
        'reviews': reviews,
        'form': form
    })


def promo_list(request):
    promo_codes = PromoCode.objects.all()
    return render(request, 'promo_list.html', {'promo_codes': promo_codes})


@login_required
def my_purchases(request):
    try:
        customer = Customer.objects.get(email=request.user.email)
        sales = Sale.objects.filter(customer=customer).order_by('-sale_date')
    except Customer.DoesNotExist:
        sales = []

    return render(request, 'my_purchases.html', {'sales': sales})


def vacancy_list(request):
    vacancies = Vacancy.objects.order_by('-published_date')
    return render(request, 'vacancies.html', {'vacancies': vacancies})


def privacy_policy(request):
    return render(request, 'privacy_policy.html')