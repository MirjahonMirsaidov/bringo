from django.contrib import admin

# Register your models here.


from .models import Manufacturer, ManufacturerTranslate, JowiManufacturer, Product, ProductTranslate, JowiProduct, Category, CategoryTranslate, JowiCategory

admin.site.register(Manufacturer)
admin.site.register(ManufacturerTranslate)
admin.site.register(JowiManufacturer)
admin.site.register(Product)
admin.site.register(ProductTranslate)
admin.site.register(JowiProduct)
admin.site.register(Category)
admin.site.register(CategoryTranslate)
admin.site.register(JowiCategory)