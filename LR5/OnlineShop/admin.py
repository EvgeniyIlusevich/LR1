from django.contrib import admin

from .models import Product, Customer, Sale, SaleProduct, Article, FAQ, Employee, PromoCode, Category, Vacancy


class SaleProductInline(admin.TabularInline):
    model = SaleProduct
    extra = 1

class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleProductInline]

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Article)
admin.site.register(Employee)
admin.site.register(PromoCode)
admin.site.register(FAQ)
admin.site.register(Vacancy)