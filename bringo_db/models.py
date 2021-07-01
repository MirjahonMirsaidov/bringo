from django.db import models


# restaurant
class Manufacturer(models.Model):
    url = models.CharField(max_length=255, blank=True, null=True)
    is_new = models.IntegerField()
    layout = models.CharField(max_length=255, blank=True, null=True)
    view = models.CharField(max_length=255, blank=True, null=True)
    min_sum = models.CharField(max_length=255)
    min_sum_order = models.FloatField()
    from_free_sum = models.FloatField()
    sum_own_delivery = models.CharField(max_length=255)
    opportunity_own_delivery = models.CharField(max_length=255)
    time_delivery = models.CharField(max_length=255)
    rating = models.IntegerField()
    votes = models.IntegerField()
    phone = models.CharField(max_length=255)
    phone_restaurant = models.CharField(max_length=50)
    phone_manager = models.CharField(max_length=255)
    courier = models.CharField(max_length=255)
    work_start = models.TimeField()
    work_finish = models.TimeField()
    status = models.IntegerField(default=1)
    is_recommended = models.IntegerField()
    is_promotion = models.IntegerField()
    site = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    created = models.DateTimeField()
    rating_total = models.IntegerField()
    is_type = models.IntegerField()
    lat = models.CharField(max_length=100, blank=True, null=True)
    lon = models.CharField(max_length=100, blank=True, null=True)
    comment = models.IntegerField(blank=True, null=True)
    delivery_status = models.IntegerField()
    min_distance = models.IntegerField()
    min_distance_limit = models.FloatField(blank=True, null=True)
    distance_limit_price = models.FloatField(blank=True, null=True)
    price_per_min_distance = models.FloatField()
    price_per_km = models.FloatField()
    prices_per_km = models.CharField(max_length=100)
    notify_param = models.CharField(max_length=15, blank=True, null=True)
    free_from = models.FloatField()
    c_min_distance = models.FloatField()
    c_price_per_min_distance = models.FloatField()
    c_prices_per_km = models.CharField(max_length=100)
    pik_prices_per_km = models.CharField(max_length=100)
    pik_time_noon = models.CharField(max_length=100)
    pik_time_launch = models.CharField(max_length=100)
    c_price_per_km = models.FloatField()
    discount_status = models.IntegerField()
    discount_date_from = models.DateTimeField(blank=True, null=True)
    discount_date_to = models.DateTimeField(blank=True, null=True)
    pik_c_prices_per_km = models.CharField(max_length=100)
    pik_c_time_noon = models.CharField(max_length=100)
    pik_c_time_launch = models.CharField(max_length=100)
    group_id = models.IntegerField(blank=True, null=True)
    show_bot = models.IntegerField()
    pik_min_distance = models.FloatField()
    pik_price_per_min_distance = models.FloatField()
    pik_c_min_distance = models.FloatField()
    pik_c_price_per_min_distance = models.FloatField()
    tracking = models.IntegerField(blank=True, null=True)
    middile_id = models.CharField(max_length=255, blank=True, null=True)
    free_delivery_discount_bringo = models.IntegerField()
    avto_zagatovka = models.IntegerField()
    sum_for_discount = models.FloatField()
    discount_for_totalsum = models.FloatField()
    delivery_discount_bringo = models.FloatField()
    is_pharmacy = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        db_table = 'StoreManufacturer'


class ManufacturerTranslate(models.Model):
    object_id = models.IntegerField()
    language_id = models.IntegerField(null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    full_description = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    payment = models.CharField(max_length=255)
    search = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'StoreManufacturerTranslate'


class JowiManufacturer(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название ресторана')
    jowi_id = models.CharField(max_length=255)
    manufacturer_id = models.CharField(max_length=255)
    status = models.IntegerField()

    def get_man_name(self):
        man_id = self.manufacturer_id
        manufacturer = ManufacturerTranslate.objects.filter(language_id=1, object_id=man_id).first()
        return manufacturer.name

    def get_man_id(self):
        man_id = self.manufacturer_id
        manufacturer = ManufacturerTranslate.objects.filter(language_id=1, object_id=man_id).first()
        return manufacturer.object_id

    class Meta:
        db_table = 'jowi_manufacturers'

    def __str__(self):
        return self.title


# meal
class Product(models.Model):
    manufacturer_id = models.IntegerField(blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    use_configurations = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=255, null=True)
    price = models.FloatField(blank=True, null=True, verbose_name='Цена')
    max_price = models.FloatField(null=True)
    is_weight = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    is_show = models.BooleanField(verbose_name='Показать продукт')
    layout = models.CharField(max_length=255, blank=True, null=True)
    view = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    quantity_order = models.IntegerField()
    availability = models.IntegerField(blank=True, null=True)
    auto_decrease_quantity = models.IntegerField(blank=True, null=True)
    work_start = models.TimeField(blank=True, null=True)
    work_finish = models.TimeField(blank=True, null=True)
    views_count = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    date_start = models.TimeField(blank=True, null=True)
    date_finish = models.TimeField(blank=True, null=True)
    added_to_cart_count = models.IntegerField(blank=True, null=True)
    votes = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    discount = models.CharField(max_length=255, blank=True, null=True)
    video = models.TextField(blank=True, null=True)
    product_to = models.IntegerField(null=True)
    product_weather_type = models.IntegerField(null=True)
    dislike = models.IntegerField(blank=True, null=True)
    like = models.IntegerField(blank=True, null=True)
    comment = models.IntegerField(blank=True, null=True)
    cook_time = models.IntegerField(blank=True, null=True)
    cook_days = models.IntegerField(blank=True, null=True)
    urgent = models.IntegerField(blank=True, null=True)
    preparation_type = models.IntegerField()
    posuda = models.CharField(max_length=20, verbose_name='Посуда')
    paket = models.CharField(max_length=20, verbose_name='Пакет')
    middile_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'StoreProduct'


class ProductTranslate(models.Model):
    object_id = models.IntegerField()
    language_id = models.IntegerField(default=1)
    name = models.CharField(max_length=255)
    short_description = models.TextField(blank=True, null=True)
    full_description = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    ingredients = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'StoreProductTranslate'

    def get_id(self):
        return int(self.object.id)

    def __str__(self):
        return self.name


class MainProductTranslate(models.Model):
    object_id = models.IntegerField()
    language_id = models.IntegerField(default=1)
    name = models.CharField(max_length=255)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'ProductTranslate'

    def get_id(self):
        return int(self.object.id)

    def __str__(self):
        return self.name


class JowiProduct(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    price = models.CharField(max_length=255)
    product_id = models.IntegerField()
    jowi_category_id = models.IntegerField()
    jowi_id = models.CharField(max_length=255)
    notification = models.IntegerField(default=False)
    modified = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_id(self):
        return int(self.bringo_product_id)

    class Meta:
        db_table = 'jowi_products'


# category
class Category(models.Model):
    lft = models.IntegerField(null=True)
    rgt = models.IntegerField(null=True)
    level = models.IntegerField(null=True)
    url = models.CharField(max_length=255, blank=True)
    full_path = models.CharField(max_length=255, blank=True)
    layout = models.CharField(max_length=255, blank=True)
    view = models.CharField(max_length=255, blank=True)
    description = models.TextField(null=True, blank=True)
    position = models.IntegerField(null=True)
    sort = models.CharField(max_length=255, blank=True)
    parent = models.IntegerField(null=True)
    sort_popularity = models.IntegerField(null=True)

    def __str__(self):
        return self.url

    class Meta:
        db_table = 'StoreCategory'


class CategoryTranslate(models.Model):
    object_id = models.IntegerField(null=True)
    language_id = models.IntegerField(null=True, default=1)
    name = models.CharField(max_length=255, null=True)
    meta_title = models.CharField(max_length=255, null=True)
    meta_keywords = models.CharField(max_length=255, null=True)
    meta_description = models.CharField(max_length=255, null=True)
    description = models.TextField(max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'StoreCategoryTranslate'


class JowiCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    category_id = models.IntegerField()
    status = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'jowi_category'


class ProductImage(models.Model):
    product_id = models.IntegerField()
    name = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255)
    is_main = models.IntegerField(default=1)
    uploaded_by = models.CharField(max_length=255, null=True, default=1)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'StoreProductImage'


class Products(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    manufacturer_id = models.IntegerField()
    position = models.CharField(max_length=255, default=0)

    class Meta:
        db_table = 'Products'


class ProductCategory(models.Model):
    product = models.IntegerField()
    category = models.IntegerField()
    is_main = models.CharField(max_length=255, default=1)

    def __str__(self):
        return self.product

    class Meta:
        db_table = 'StoreProductCategoryRef'


class ManufacturerCategory(models.Model):
    manufacturer_id = models.IntegerField()
    category_id = models.IntegerField()

    class Meta:
        db_table = 'StoreManufacturerCategoryRef'


class StoreProductProduct(models.Model):
    store_product_id = models.IntegerField()
    product_id = models.IntegerField()
    option_id = models.IntegerField(null=True)
    is_default = models.CharField(max_length=255, default=1)

    def __str__(self):
        return self.store_product_id

    class Meta:
        db_table = 'StoreProductProductRef'






