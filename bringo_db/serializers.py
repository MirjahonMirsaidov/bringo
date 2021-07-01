from rest_framework import serializers
from .models import Manufacturer, JowiManufacturer, ManufacturerTranslate, Category, CategoryTranslate, JowiCategory, \
    JowiProduct, ProductTranslate, Product, ProductImage, ManufacturerCategory


class ManufacturerSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    url = serializers.CharField(required=False, max_length=255, allow_null=True)
    is_new = serializers.IntegerField(required=False)
    layout = serializers.CharField(required=False, max_length=255, allow_null=True)
    view = serializers.CharField(required=False, max_length=255, allow_null=True)
    min_sum = serializers.CharField(max_length=255)
    min_sum_order = serializers.FloatField()
    from_free_sum = serializers.FloatField()
    sum_own_delivery = serializers.CharField(max_length=255)
    opportunity_own_delivery = serializers.CharField(max_length=255, allow_blank=True)
    time_delivery = serializers.CharField(max_length=255)
    rating = serializers.IntegerField()
    votes = serializers.IntegerField()
    phone = serializers.CharField(max_length=255)
    phone_restaurant = serializers.CharField(max_length=50, allow_blank=True)
    phone_manager = serializers.CharField(max_length=255, allow_blank=True)
    courier = serializers.CharField(max_length=255, allow_blank=True)
    work_start = serializers.TimeField()
    work_finish = serializers.TimeField()
    status = serializers.IntegerField()
    is_recommended = serializers.IntegerField()
    is_promotion = serializers.IntegerField()
    site = serializers.CharField(max_length=255, allow_blank=True)
    email = serializers.CharField(max_length=255, allow_blank=True)
    contact_name = serializers.CharField(max_length=255, allow_blank=True)
    created = serializers.DateTimeField()
    rating_total = serializers.IntegerField()
    is_type = serializers.IntegerField()
    lat = serializers.CharField(max_length=100, allow_null=True)
    lon = serializers.CharField(max_length=100, allow_null=True)
    comment = serializers.IntegerField(allow_null=True)
    delivery_status = serializers.IntegerField()
    min_distance = serializers.IntegerField()
    min_distance_limit = serializers.FloatField(allow_null=True)
    distance_limit_price = serializers.FloatField(allow_null=True)
    price_per_min_distance = serializers.FloatField()
    price_per_km = serializers.FloatField()
    prices_per_km = serializers.CharField(max_length=100, allow_blank=True)
    notify_param = serializers.CharField(max_length=15, allow_null=True, allow_blank=True)
    free_from = serializers.FloatField()
    c_min_distance = serializers.FloatField()
    c_price_per_min_distance = serializers.FloatField()
    c_prices_per_km = serializers.CharField(max_length=100, allow_blank=True)
    pik_prices_per_km = serializers.CharField(max_length=100, allow_blank=True)
    pik_time_noon = serializers.CharField(max_length=100, allow_blank=True)
    pik_time_launch = serializers.CharField(max_length=100, allow_blank=True)
    c_price_per_km = serializers.FloatField()
    discount_status = serializers.IntegerField()
    discount_date_from = serializers.DateTimeField(allow_null=True)
    discount_date_to = serializers.DateTimeField(allow_null=True)
    pik_c_prices_per_km = serializers.CharField(max_length=100, allow_blank=True)
    pik_c_time_noon = serializers.CharField(max_length=100, allow_blank=True)
    pik_c_time_launch = serializers.CharField(max_length=100, allow_blank=True)
    group_id = serializers.IntegerField(allow_null=True)
    show_bot = serializers.IntegerField()
    pik_min_distance = serializers.FloatField()
    pik_price_per_min_distance = serializers.FloatField()
    pik_c_min_distance = serializers.FloatField()
    pik_c_price_per_min_distance = serializers.FloatField()
    tracking = serializers.IntegerField(allow_null=True)
    middile_id = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    free_delivery_discount_bringo = serializers.IntegerField()
    avto_zagatovka = serializers.IntegerField()
    sum_for_discount = serializers.FloatField()
    discount_for_totalsum = serializers.FloatField()
    delivery_discount_bringo = serializers.FloatField()
    is_pharmacy = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def create(self, validated_data):
        return Manufacturer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance.title = validated_data.get('title', instance.title)
        # instance.description = validated_data.get('description', instance.description)
        # instance.body = validated_data.get('body', instance.body)
        # instance.author_id = validated_data.get('author_id', instance.author_id)
        # instance.save()
        return instance


class ManufacturerTranslateSerializer(serializers.Serializer):
    object_id = serializers.IntegerField()
    language_id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(max_length=255, allow_null=True)
    description = serializers.CharField(allow_null=True)
    full_description = serializers.CharField(allow_null=True)
    meta_title = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    meta_keywords = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    meta_description = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    payment = serializers.CharField(max_length=255)
    search = serializers.CharField(max_length=255, allow_blank=True)

    def create(self, validated_data):
        return ManufacturerTranslate.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance


class JowiManufacturerSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    jowi_id = serializers.CharField(max_length=255)
    manufacturer_id = serializers.CharField(max_length=255)
    status = serializers.IntegerField()

    def create(self, validated_data):
        return JowiManufacturer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance.objects.update(**validated_data)


class CategorySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    lft = serializers.IntegerField(allow_null=True)
    rgt = serializers.IntegerField(allow_null=True)
    level = serializers.IntegerField(allow_null=True)
    url = serializers.CharField(max_length=255, allow_blank=True)
    full_path = serializers.CharField(max_length=255, allow_blank=True)
    layout = serializers.CharField(max_length=255, allow_blank=True)
    view = serializers.CharField(max_length=255, allow_blank=True)
    description = serializers.CharField(allow_null=True)
    position = serializers.IntegerField()
    sort = serializers.CharField(max_length=255, allow_blank=True)
    parent = serializers.IntegerField()
    sort_popularity = serializers.IntegerField()

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance.objects.update(**validated_data)


class CategoryTranslateSerializer(serializers.Serializer):
    object_id = serializers.IntegerField(allow_null=True)
    language_id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(max_length=255)
    meta_title = serializers.CharField(max_length=255)
    meta_keywords = serializers.CharField(max_length=255)
    meta_description = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return CategoryTranslate.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance.objects.update(**validated_data)


class JowiCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    category_id = serializers.IntegerField()
    status = serializers.IntegerField()

    def create(self, validated_data):
        return JowiCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance.objects.update(**validated_data)


class ProductSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    manufacturer_id = serializers.IntegerField(allow_null=True)
    type_id = serializers.IntegerField(allow_null=True)
    use_configurations = serializers.IntegerField()
    url = serializers.CharField(allow_blank=True, max_length=255)
    price = serializers.FloatField(allow_null=True)
    max_price = serializers.FloatField()
    is_weight = serializers.IntegerField(allow_null=True)
    is_active = serializers.BooleanField()
    is_show = serializers.BooleanField()
    layout = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    view = serializers.CharField(allow_blank=True, max_length=255, allow_null=True)
    sku = serializers.CharField(allow_blank=True, max_length=255, allow_null=True)
    quantity = serializers.IntegerField(allow_null=True)
    quantity_order = serializers.IntegerField()
    availability = serializers.IntegerField(allow_null=True)
    auto_decrease_quantity = serializers.IntegerField(allow_null=True)
    work_start = serializers.TimeField(allow_null=True)
    work_finish = serializers.TimeField(allow_null=True)
    views_count = serializers.IntegerField(allow_null=True)
    created = serializers.DateTimeField(allow_null=True)
    updated = serializers.DateTimeField(allow_null=True)
    date_start = serializers.TimeField(allow_null=True)
    date_finish = serializers.TimeField(allow_null=True)
    added_to_cart_count = serializers.IntegerField(allow_null=True)
    votes = serializers.IntegerField()
    rating = serializers.IntegerField()
    discount = serializers.CharField(allow_blank=True, max_length=255, allow_null=True)
    video = serializers.CharField(allow_blank=True, allow_null=True)
    product_to = serializers.IntegerField()
    product_weather_type = serializers.IntegerField()
    dislike = serializers.IntegerField(allow_null=True)
    like = serializers.IntegerField(allow_null=True)
    comment = serializers.IntegerField(allow_null=True)
    cook_time = serializers.IntegerField(allow_null=True)
    cook_days = serializers.IntegerField(allow_null=True)
    urgent = serializers.IntegerField(allow_null=True)
    preparation_type = serializers.IntegerField()
    posuda = serializers.CharField(allow_blank=True, max_length=20)
    paket = serializers.CharField(allow_blank=True, max_length=20)
    middile_id = serializers.CharField(allow_blank=True, max_length=255, allow_null=True)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance.objects.update(**validated_data)


class ProductTranslateSerializer(serializers.Serializer):
    object_id = serializers.IntegerField()
    language_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    short_description = serializers.CharField(allow_null=True)
    full_description = serializers.CharField(allow_null=True)
    meta_title = serializers.CharField(max_length=255, allow_null=True)
    meta_keywords = serializers.CharField(max_length=255, allow_null=True)
    meta_description = serializers.CharField(max_length=255, allow_null=True)
    ingredients = serializers.CharField(allow_blank=True, max_length=255, allow_null=True)

    def create(self, validated_data):
        return ProductTranslate.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance.objects.update(**validated_data)


class JowiProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    price = serializers.CharField(max_length=255)
    product_id = serializers.IntegerField()
    jowi_category_id = serializers.IntegerField()
    jowi_id = serializers.CharField(max_length=255)
    notification = serializers.IntegerField()

    def create(self, validated_data):
        return JowiProduct.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance.objects.update(**validated_data)


class ProductImageSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    is_main = serializers.IntegerField()
    uploaded_by = serializers.CharField(max_length=255)
    date_uploaded = serializers.DateTimeField()
    title = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return ProductImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance.objects.update(**validated_data)


class ManufacturerCategorySerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    manufacturer_id = serializers.IntegerField()

    def create(self, validated_data):
        return ProductImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance.objects.update(**validated_data)
