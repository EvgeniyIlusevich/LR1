from decimal import Decimal
from unittest.mock import patch, Mock
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import (
    Category, Product, Customer, Sale, SaleProduct,
    Article, FAQ, Employee, PromoCode, Vacancy, Review
)
from .forms import ProductEdit, ReviewForm, SaleProductForm, CustomUserCreationForm


class ModelTests(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Smartphone",
            price=Decimal("500.00"),
            unit="pcs",
            category=self.category
        )
        self.user = User.objects.create_user(
            username="testuser", password="12345",
            email="test@example.com", first_name="Test", last_name="User"
        )
        self.customer = Customer.objects.create(
            first_name="Test", last_name="User",
            email="test@example.com", phone="+375291234567"
        )
        
    def test_category_str(self):
        self.assertEqual(str(self.category), "Electronics")
        
    def test_product_str(self):
        self.assertEqual(str(self.product), "Smartphone")
        
    def test_customer_str(self):
        self.assertEqual(str(self.customer), "Test User")
        
    def test_sale_str(self):
        sale = Sale.objects.create(
            customer=self.customer,
            delivery_date=timezone.now() + timedelta(days=7),
            city="Minsk"
        )
        self.assertIn(str(sale.id), str(sale))
        
    def test_saleproduct_str(self):
        sale = Sale.objects.create(
            customer=self.customer,
            delivery_date=timezone.now() + timedelta(days=7),
            city="Minsk"
        )
        sp = SaleProduct.objects.create(
            sale=sale, product=self.product, quantity=2, price=self.product.price
        )
        self.assertIn(str(sp.id), str(sp))
        
    def test_article_str(self):
        article = Article.objects.create(
            title="Test Article", publication_date=date.today(),
            summary="Summary", content="Content", author="Author"
        )
        self.assertEqual(str(article), "Test Article")
        
    def test_faq_str(self):
        faq = FAQ.objects.create(question="Q?", answer="A")
        self.assertEqual(str(faq), "Q?")
        
    def test_employee_str(self):
        emp = Employee.objects.create(
            name="John", job_description="Dev", phone="+375291234567", email="a@b.com"
        )
        self.assertEqual(str(emp), "John")
        
    def test_promocode_str(self):
        promo = PromoCode.objects.create(code="DISCOUNT10", discount_percent=10)
        self.assertEqual(str(promo), "DISCOUNT10")
        
    def test_vacancy_str(self):
        vac = Vacancy.objects.create(title="Developer", description="Desc")
        self.assertEqual(str(vac), "Developer")
        
    def test_review_str(self):
        review = Review.objects.create(
            product=self.product, author=self.user,
            text="Great", rating=5
        )
        self.assertEqual(str(review), f"Review for Smartphone by testuser")


class FormTests(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name="Books")
        
    def test_product_edit_form_valid(self):
        form_data = {
            "name": "New Product",
            "price": "99.99",
            "unit": "pcs",
            "category": self.category.id
        }
        form = ProductEdit(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_product_edit_form_invalid(self):
        form = ProductEdit(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        
    def test_review_form_valid(self):
        form = ReviewForm(data={"text": "Good product", "rating": 4})
        self.assertTrue(form.is_valid())
        
    def test_review_form_rating_too_high(self):
        form = ReviewForm(data={"text": "Bad", "rating": 11})
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)
        
    def test_review_form_rating_too_low(self):
        form = ReviewForm(data={"text": "Bad", "rating": 0})
        self.assertFalse(form.is_valid())
        
    def test_sale_product_form_valid(self):
        form = SaleProductForm(data={"city": "Minsk", "quantity": 2, "promo_code": "SAVE10"})
        self.assertTrue(form.is_valid())
        
    def test_sale_product_form_quantity_minimum(self):
        form = SaleProductForm(data={"city": "Minsk", "quantity": 0, "promo_code": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)
        
    def test_custom_user_creation_form_valid(self):
        form_data = {
            "username": "newuser",
            "email": "new@example.com",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "phone": "+375291234567",
            "birth_date": "2000-01-01",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_custom_user_creation_form_age_too_young(self):
        form_data = {
            "username": "younguser",
            "email": "young@example.com",
            "first_name": "Petr",
            "last_name": "Petrov",
            "phone": "+375291234567",
            "birth_date": (date.today() - timedelta(days=365*16)).isoformat(),
            "password1": "ComplexPass123",
            "password2": "ComplexPass123"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("birth_date", form.errors)
        
    def test_custom_user_creation_form_invalid_phone(self):
        form_data = {
            "username": "phoneuser",
            "email": "phone@example.com",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "phone": "12345",
            "birth_date": "2000-01-01",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)


class ViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop", price=Decimal("1200.00"), unit="pcs", category=self.category
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpass",
            email="test@example.com", first_name="Test", last_name="User"
        )
        self.customer = Customer.objects.create(
            first_name="Test", last_name="User",
            email="test@example.com", phone="+375291234567"
        )
        self.staff_user = User.objects.create_user(
            username="staffuser", password="staffpass",
            email="staff@example.com", is_staff=True
        )
        
    def test_product_list_view(self):
        response = self.client.get(reverse('products_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Laptop")
        
    def test_product_list_filter_by_price(self):
        response = self.client.get(reverse('products_list'), {"min_price": "1000", "max_price": "1500"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Laptop")
        
    def test_create_product_view_post_valid(self):
        self.client.login(username="testuser", password="testpass")
        post_data = {
            "name": "Tablet",
            "price": "300.00",
            "unit": "pcs",
            "category": self.category.id
        }
        response = self.client.post(reverse('create_product'), data=post_data)
        self.assertRedirects(response, reverse('products_list'))
        self.assertTrue(Product.objects.filter(name="Tablet").exists())
        
    def test_edit_product_view_get(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse('edit_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], self.product)
        
    def test_edit_product_view_post(self):
        self.client.login(username="testuser", password="testpass")
        post_data = {
            "name": "Updated Laptop",
            "price": "1100.00",
            "unit": "kg",
            "category": self.category.id
        }
        response = self.client.post(reverse('edit_product', args=[self.product.id]), data=post_data)
        self.assertRedirects(response, reverse('products_list'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Laptop")
        self.assertEqual(self.product.price, Decimal("1100.00"))
        
    def test_delete_product_view_post(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse('delete_product', args=[self.product.id]))
        self.assertRedirects(response, reverse('products_list'))
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
        
    def test_buy_product_view_get(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse('buy_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Laptop")
        
    def test_buy_product_with_valid_promo(self):
        self.client.login(username="testuser", password="testpass")
        PromoCode.objects.create(code="SAVE20", discount_percent=20, active=True)
        post_data = {
            "city": "Minsk",
            "quantity": "2",
            "promo_code": "SAVE20"
        }
        response = self.client.post(reverse('buy_product', args=[self.product.id]), data=post_data)
        self.assertRedirects(response, reverse('products_list'))
        sale = Sale.objects.filter(customer=self.customer).first()
        self.assertIsNotNone(sale)
        sp = SaleProduct.objects.filter(sale=sale).first()
        self.assertEqual(sp.quantity, 2)
        expected_price = self.product.price * Decimal("0.8")
        self.assertAlmostEqual(sp.price, expected_price, places=2)
        self.assertEqual(sale.total_price, expected_price * 2)
        
    def test_buy_product_with_invalid_promo(self):
        self.client.login(username="testuser", password="testpass")
        post_data = {
            "city": "Minsk",
            "quantity": "1",
            "promo_code": "INVALID"
        }
        response = self.client.post(reverse('buy_product', args=[self.product.id]), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'promo_code', 'Промокод недействителен или неактивен')
        
    def test_sale_list_empty(self):
        self.client.login(username="staffuser", password="staffpass")
        response = self.client.get(reverse('sale_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('sales_mean', response.context)
        
    def test_sale_list_with_sales(self):
        self.client.login(username="staffuser", password="staffpass")
        # Удаляем все продажи из фикстуры, чтобы они не влияли на расчёт
        Sale.objects.all().delete()
        SaleProduct.objects.all().delete()
        sale = Sale.objects.create(
            customer=self.customer, delivery_date=timezone.now() + timedelta(days=7), city="Minsk"
        )
        SaleProduct.objects.create(
            sale=sale, product=self.product, quantity=3, price=self.product.price
        )
        sale.total_price = self.product.price * 3
        sale.save()
        
        response = self.client.get(reverse('sale_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('sales', response.context)
        self.assertTrue(response.context['sales'].filter(id=sale.id).exists())
        self.assertIn('most_popular_type', response.context)
        self.assertEqual(response.context['most_popular_type'], "Electronics")
        
    def test_article_list(self):
        Article.objects.create(
            title="Article1", publication_date=date.today(),
            summary="Sum", content="Cont", author="Auth"
        )
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Article1")
        
    def test_article_detail(self):
        article = Article.objects.create(
            title="Detail", publication_date=date.today(),
            summary="Sum", content="Content", author="Auth"
        )
        response = self.client.get(reverse('article_detail', args=[article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['article'], article)
        
    def test_latest_article(self):
        art1 = Article.objects.create(
            title="Old", publication_date=date(2020,1,1),
            summary="S", content="C", author="A"
        )
        art2 = Article.objects.create(
            title="New", publication_date=date.today(),
            summary="S", content="C", author="A"
        )
        response = self.client.get(reverse('latest_article'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['article'], art2)
        
    def test_faq_list(self):
        FAQ.objects.create(question="Q1", answer="A1")
        response = self.client.get(reverse('faq_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Q1")
        
    def test_contact_list(self):
        Employee.objects.create(
            name="John", job_description="Dev", phone="+375291234567", email="j@j.com"
        )
        response = self.client.get(reverse('contact_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John")
        
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)
        
    def test_register_view_post_valid(self):
        post_data = {
            "username": "newuser2",
            "email": "new2@example.com",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "phone": "+375291234567",
            "birth_date": "2000-01-01",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123"
        }
        response = self.client.post(reverse('register'), data=post_data)
        self.assertRedirects(response, reverse('about_us'))
        user = User.objects.get(username="newuser2")
        self.assertTrue(user.is_authenticated)
        self.assertTrue(Customer.objects.filter(email="new2@example.com").exists())
        
    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
    def test_login_view_post_valid(self):
        post_data = {"username": "testuser", "password": "testpass"}
        response = self.client.post(reverse('login'), data=post_data)
        self.assertRedirects(response, reverse('about_us'))
        
    def test_logout_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        
    def test_product_reviews_get(self):
        response = self.client.get(reverse('product_reviews', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], self.product)
        
    def test_product_reviews_post_valid(self):
        self.client.login(username="testuser", password="testpass")
        post_data = {"text": "Good product!", "rating": 5}
        response = self.client.post(reverse('product_reviews', args=[self.product.id]), data=post_data)
        self.assertRedirects(response, reverse('product_reviews', args=[self.product.id]))
        self.assertTrue(Review.objects.filter(product=self.product, author=self.user).exists())
        
    def test_promo_list(self):
        PromoCode.objects.create(code="SAVE10", discount_percent=10, active=True)
        response = self.client.get(reverse('promo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SAVE10")
        
    def test_my_purchases_authenticated(self):
        self.client.login(username="testuser", password="testpass")
        sale = Sale.objects.create(
            customer=self.customer, delivery_date=timezone.now() + timedelta(days=7), city="Minsk"
        )
        response = self.client.get(reverse('my_purchases'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('sales', response.context)
        self.assertEqual(len(response.context['sales']), 1)
        
    def test_my_purchases_unauthenticated_redirect(self):
        response = self.client.get(reverse('my_purchases'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)
        
    def test_vacancy_list(self):
        Vacancy.objects.create(title="Python Dev", description="Desc", salary=1000)
        response = self.client.get(reverse('vacancy_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Dev")
        
    def test_about_us(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)
        
    def test_privacy_policy(self):
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)
        
    @patch('OnlineShop.views.get_random_joke')
    def test_rand_page_with_joke(self, mock_joke):
        mock_joke.return_value = "Why did the developer go broke? Because he used up all his cache!"
        response = self.client.get(reverse('rand'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Why did the developer go broke?")
        
    @patch('OnlineShop.views.get_random_gif')
    def test_gif_page_with_gif(self, mock_gif):
        mock_gif.return_value = "https://media.giphy.com/.../random.gif"
        response = self.client.get(reverse('gif'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "https://media.giphy.com")


class ExternalApiTests(TestCase):
    
    @patch('OnlineShop.views.requests.get')
    def test_get_random_gif_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": {"images": {"original": {"url": "https://gif.url"}}}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        from .views import get_random_gif
        url = get_random_gif()
        self.assertEqual(url, "https://gif.url")
        
    @patch('OnlineShop.views.requests.get')
    def test_get_random_joke_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"setup": "Why?", "punchline": "Because!"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        from .views import get_random_joke
        joke = get_random_joke()
        self.assertEqual(joke, "Why? - Because!")